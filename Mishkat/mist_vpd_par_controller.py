#!/usr/bin/env python3
import os, csv, time, math, logging, io
from datetime import datetime, timezone
from typing import Optional, Tuple

# ================= CONFIG =================
CSV_DIR = "/home/cdacea/climate"
CSV_Z1  = os.path.join(CSV_DIR, "Zone1_minute.csv")
CSV_Z3  = os.path.join(CSV_DIR, "Zone3_minute.csv")
LOGFILE = os.path.join(CSV_DIR, "mist_vpd_par_controller.log")
ACTIONS_CSV = os.path.join(CSV_DIR, "mist_actions.csv")

# GPIO (BCM numbering). Change to your wiring.
PUMP_PIN = 17
Z1_PIN   = 27
Z3_PIN   = 22
ACTIVE_HIGH = False     # set False if your relays are active-LOW

# Sequencing
VALVE_LEAD_SEC = 1.0    # valve on before pump
PUMP_LAG_SEC   = 0.0    # pump off at same time valve closes

# Data freshness
MAX_DATA_AGE_SEC = 5 * 60   # stale if older than 5 minutes

# Controller cadence
SCHED_TICK_SEC = 5

# DRY RUN (no GPIO toggles; logs only)
DRY_RUN = False

# ================= LOGGING =================
os.makedirs(CSV_DIR, exist_ok=True)
logging.basicConfig(
    filename=LOGFILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logging.info("🌿 mist_vpd_par_controller starting")

# Ensure actions CSV header
if not os.path.exists(ACTIONS_CSV) or os.path.getsize(ACTIONS_CSV) == 0:
    try:
        with open(ACTIONS_CSV, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["datetime_utc", "zone", "vpd", "par", "duration_sec", "next_wait_sec"])
    except Exception as e:
        logging.error(f"Could not initialize actions CSV: {e}")

# ================= GPIO =================
pump = z1 = z3 = None
try:
    if not DRY_RUN:
        from gpiozero import OutputDevice
        pump = OutputDevice(PUMP_PIN, active_high=ACTIVE_HIGH, initial_value=False)
        z1   = OutputDevice(Z1_PIN,   active_high=ACTIVE_HIGH, initial_value=False)
        z3   = OutputDevice(Z3_PIN,   active_high=ACTIVE_HIGH, initial_value=False)
    else:
        logging.info("DRY_RUN enabled — no GPIO will be toggled.")
except Exception as e:
    logging.error(f"GPIO init failed: {e}; forcing DRY_RUN.")
    DRY_RUN = True

# ================= Helpers =================
def parse_iso(ts: str) -> Optional[datetime]:
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except Exception:
        return None

def read_latest_avg(csv_path: str) -> Tuple[Optional[float], Optional[float], Optional[datetime]]:
    """Read last line, strip NULs, parse VPD_avg + PAR_avg."""
    if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
        return (None, None, None)
    try:
        with open(csv_path, "rb") as fb:
            raw = fb.read()
        if b"\x00" in raw:
            logging.warning(f"NUL bytes found in {csv_path}; sanitizing")
            raw = raw.replace(b"\x00", b"")
        text = raw.decode("utf-8", errors="replace")

        lines = [ln for ln in text.splitlines() if ln.strip()]
        if len(lines) < 2:
            return (None, None, None)

        header = next(csv.reader([lines[0]]))
        row    = next(csv.reader([lines[-1]]))

        def find(col):
            for i, h in enumerate(header):
                if h.strip() == col:
                    return i
            low = [h.strip().lower() for h in header]
            return low.index(col.lower()) if col.lower() in low else -1

        i_dt  = find("datetime")
        i_vpd = find("VPD_avg")
        i_par = find("PAR_avg")
        if min(i_dt, i_vpd, i_par) < 0 or max(i_dt, i_vpd, i_par) >= len(row):
            return (None, None, None)

        ts = parse_iso(row[i_dt].strip())
        def to_float(s):
            try:
                s = s.strip()
                if s == "" or s.lower() == "nan":
                    return math.nan
                return float(s)
            except:
                return math.nan
        vpd = to_float(row[i_vpd])
        par = to_float(row[i_par])
        if math.isnan(vpd) or math.isnan(par):
            return (None, None, None)

        return (vpd, par, ts)

    except Exception as e:
        logging.error(f"CSV read error {csv_path}: {e}")
        return (None, None, None)

def fresh(ts: Optional[datetime]) -> bool:
    if not ts: return False
    if ts.tzinfo is None: ts = ts.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - ts).total_seconds() <= MAX_DATA_AGE_SEC

def pick_mist_duration(vpd: float) -> Optional[float]:
    if vpd is None: return None
    if 0.7 <= vpd < 1.0: return 7.0
    if 1.0 <= vpd < 1.5: return 9.0
    if 1.5 <= vpd < 2.5: return 11.0
    return None

def pick_wait_interval(par: float) -> Optional[float]:
    if par is None: return None
    if par < 200.0: return None
    if 1000.0 <= par < 2000.0: return 15 * 60
    if  800.0 <= par < 1000.0: return 20 * 60
    if  600.0 <= par <  800.0: return 30 * 60
    if  400.0 <= par <  600.0: return 45 * 60
    if  200.0 <= par <  400.0: return 60 * 60
    if par >= 2000.0: return 15 * 60
    return None

def dev_set(dev, name: str, on: bool):
    if DRY_RUN or dev is None:
        logging.info(f"[DRY] {name} -> {'ON' if on else 'OFF'}")
        return
    try:
        dev.on() if on else dev.off()
        logging.info(f"{name} -> {'ON' if on else 'OFF'}")
    except Exception as e:
        logging.error(f"GPIO toggle failed for {name}: {e}")

def log_action(zone_name: str, vpd: float, par: float, dur: float, wait_sec: float):
    try:
        ts = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        with open(ACTIONS_CSV, "a", newline="") as f:
            w = csv.writer(f)
            w.writerow([ts, zone_name,
                        f"{vpd:.2f}" if vpd is not None else "",
                        f"{par:.1f}" if par is not None else "",
                        f"{dur:.1f}", int(wait_sec)])
    except Exception as e:
        logging.error(f"Failed to write actions CSV: {e}")

# ================= Scheduler =================
next_ok = {"z1": 0.0, "z3": float("inf")}  # z3 disabled
state_pump = False
last_valve_closed_t = 0.0

def run_mist(zone_name: str, valve_dev, vpd: float, par: float):
    global state_pump, last_valve_closed_t
    dur  = pick_mist_duration(vpd)
    wait = pick_wait_interval(par)
    if dur is None or wait is None:
        logging.info(f"{zone_name}: skip (VPD={vpd}, PAR={par}); reschedule")
        next_ok[zone_name] = time.monotonic() + (wait if wait else 5*60)
        return

    logging.info(f"{zone_name}: MIST start — VPD={vpd:.2f}, PAR={par:.1f}, dur={dur}s, next_wait={int(wait/60)}m")

    # Open valve first
    dev_set(valve_dev, f"{zone_name.upper()}_VALVE", True)
    time.sleep(VALVE_LEAD_SEC)

    # Then pump on
    if not state_pump:
        dev_set(pump, "PUMP", True)
        state_pump = True

    # Continue misting for the duration (minus the 1s lead already elapsed)
    time.sleep(max(0.0, dur - VALVE_LEAD_SEC))

    # Close valve and pump together
    dev_set(valve_dev, f"{zone_name.upper()}_VALVE", False)
    last_valve_closed_t = time.monotonic()
    if state_pump:
        dev_set(pump, "PUMP", False)
        state_pump = False

    log_action(zone_name, vpd, par, dur, wait)

    next_ok[zone_name] = time.monotonic() + wait
    logging.info(f"{zone_name}: MIST end — next eligible in {int(wait/60)} min")

# ================= Main loop =================
try:
    while True:
        now_mono = time.monotonic()
        z1_ready = now_mono >= next_ok["z1"]
        z3_ready = now_mono >= next_ok["z3"]

        to_try = []
        if z1_ready: to_try.append(("z1", CSV_Z1, z1))
        if z3_ready: to_try.append(("z3", CSV_Z3, z3))

        did_any = False
        for name, csv_path, dev in to_try:
            vpd, par, ts = read_latest_avg(csv_path)
            ok = (vpd is not None) and (par is not None) and fresh(ts)
            if not ok:
                logging.info(f"{name}: data not ready (vpd={vpd}, par={par}, fresh={fresh(ts)}); retry in 5 min")
                next_ok[name] = now_mono + 5*60
                continue
            run_mist(name, dev, vpd, par)
            did_any = True
            break  # only one zone per cycle

        time.sleep(SCHED_TICK_SEC)

except KeyboardInterrupt:
    logging.info("Stopping controller (KeyboardInterrupt).")
finally:
    try:
        dev_set(z1, "Z1_VALVE", False)
        dev_set(z3, "Z3_VALVE", False)
        time.sleep(PUMP_LAG_SEC)
        dev_set(pump, "PUMP", False)
    except Exception:
        pass
