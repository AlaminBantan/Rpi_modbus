#!/usr/bin/env python3
import os, csv, time, math, logging
from datetime import datetime, time as dtime, timezone
from typing import Optional, Tuple
from zoneinfo import ZoneInfo  # Python 3.9+

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

# Time window (local KSA)
KSA_TZ = ZoneInfo("Asia/Riyadh")
WINDOW_START = dtime(8, 0, 0)   # 08:00
WINDOW_END   = dtime(18, 0, 0)  # 18:00

# ================= LOGGING =================
os.makedirs(CSV_DIR, exist_ok=True)
logging.basicConfig(
    filename=LOGFILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logging.info("🌿 mist_vpd_par_controller (Plant VPD) starting")

# Ensure actions CSV header
if not os.path.exists(ACTIONS_CSV) or os.path.getsize(ACTIONS_CSV) == 0:
    try:
        with open(ACTIONS_CSV, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["datetime_utc", "zone", "plant_vpd", "par", "duration_sec", "next_wait_sec"])
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

def find_col_index(header, want: str) -> int:
    # exact first
    for i, h in enumerate(header):
        if h.strip() == want:
            return i
    # case-insensitive fallback
    lower = [h.strip().lower() for h in header]
    return lower.index(want.lower()) if want.lower() in lower else -1

def to_float(s: str) -> float:
    try:
        s = s.strip()
        if s == "" or s.lower() == "nan":
            return math.nan
        return float(s)
    except Exception:
        return math.nan

def svp_kpa(temp_c: float) -> float:
    # Tetens formula (kPa)
    return 0.6108 * math.exp((17.27 * temp_c) / (temp_c + 237.3))

def compute_plant_vpd_from_air(temp_air_c: float, rh_pct: float, leaf_delta_c: float = -2.0) -> float:
    if math.isnan(temp_air_c) or math.isnan(rh_pct):
        return math.nan
    t_leaf = temp_air_c + leaf_delta_c
    es_leaf = svp_kpa(t_leaf)
    # VPD ≈ es_leaf - ea; with ea ≈ RH * es_air
    es_air = svp_kpa(temp_air_c)
    ea = (rh_pct / 100.0) * es_air
    vpd = es_leaf - ea
    return max(0.0, vpd)

def read_latest_avg(csv_path: str) -> Tuple[Optional[float], Optional[float], Optional[float], Optional[float], Optional[datetime]]:
    """
    Read last line, strip NULs.
    Returns: (plant_vpd, par, temp_air, rh, timestamp)
    - Prefer 'PlantVPD_avg' column if present.
    - Else compute Plant VPD from Temp_avg - 2°C and RH_avg.
    """
    if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
        return (None, None, None, None, None)
    try:
        with open(csv_path, "rb") as fb:
            raw = fb.read()
        if b"\x00" in raw:
            logging.warning(f"NUL bytes found in {csv_path}; sanitizing")
            raw = raw.replace(b"\x00", b"")
        text = raw.decode("utf-8", errors="replace")

        lines = [ln for ln in text.splitlines() if ln.strip()]
        if len(lines) < 2:
            return (None, None, None, None, None)

        header = next(csv.reader([lines[0]]))
        row    = next(csv.reader([lines[-1]]))

        i_dt   = find_col_index(header, "datetime")
        i_par  = find_col_index(header, "PAR_avg")
        i_t    = find_col_index(header, "Temp_avg")
        i_rh   = find_col_index(header, "RH_avg")

        # Plant VPD column may already exist
        i_pvpd = find_col_index(header, "PlantVPD_avg")

        if i_dt < 0 or i_par < 0 or i_t < 0 or i_rh < 0:
            return (None, None, None, None, None)

        ts = parse_iso(row[i_dt].strip())
        par = to_float(row[i_par])
        t_air = to_float(row[i_t])
        rh = to_float(row[i_rh])

        if i_pvpd >= 0 and i_pvpd < len(row):
            plant_vpd = to_float(row[i_pvpd])
        else:
            plant_vpd = compute_plant_vpd_from_air(t_air, rh, leaf_delta_c=-2.0)

        if any(math.isnan(x) for x in [par, t_air, rh, plant_vpd]):
            return (None, None, None, None, None)

        return (plant_vpd, par, t_air, rh, ts)

    except Exception as e:
        logging.error(f"CSV read error {csv_path}: {e}")
        return (None, None, None, None, None)

def fresh(ts: Optional[datetime]) -> bool:
    if not ts: return False
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - ts).total_seconds() <= MAX_DATA_AGE_SEC

def within_time_window(now_local: datetime) -> bool:
    t = now_local.timetz()
    # simple inclusive start, exclusive end
    return (t >= WINDOW_START and t < WINDOW_END)

# ----- Duration by Plant VPD -----
def pick_mist_duration(plant_vpd: float) -> Optional[float]:
    if plant_vpd is None or math.isnan(plant_vpd):
        return None
    if 0.8 <= plant_vpd < 1.0: return 8.0
    if 1.0 <= plant_vpd < 1.5: return 10.0
    if 1.5 <= plant_vpd < 2.0: return 12.0
    return None  # outside mist bands

# ----- Cooldown by PAR -----
def pick_wait_interval(par: float) -> Optional[float]:
    if par is None or math.isnan(par): return None
    if par < 300.0: return None  # guardrail will already block misting
    if 1500.0 <= par:            return 15 * 60
    if 1200.0 <= par < 1500.0:   return 15 * 60
    if 1000.0 <= par < 1200.0:   return 20 * 60
    if  800.0 <= par < 1000.0:   return 30 * 60
    if  600.0 <= par <  800.0:   return 45 * 60
    if  300.0 <= par <  600.0:   return 60 * 60
    return None

def guardrails_ok(par: float, t_air: float, rh: float) -> bool:
    if any(math.isnan(x) for x in [par, t_air, rh]): return False
    if par < 300.0: return False
    if not (20.0 <= t_air < 32.0): return False
    if not (40.0 <= rh   < 80.0):  return False
    return True

def dev_set(dev, name: str, on: bool):
    if DRY_RUN or dev is None:
        logging.info(f"[DRY] {name} -> {'ON' if on else 'OFF'}")
        return
    try:
        dev.on() if on else dev.off()
        logging.info(f"{name} -> {'ON' if on else 'OFF'}")
    except Exception as e:
        logging.error(f"GPIO toggle failed for {name}: {e}")

def log_action(zone_name: str, plant_vpd: float, par: float, dur: float, wait_sec: float):
    try:
        ts = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        with open(ACTIONS_CSV, "a", newline="") as f:
            w = csv.writer(f)
            w.writerow([ts, zone_name,
                        f"{plant_vpd:.2f}" if plant_vpd is not None else "",
                        f"{par:.1f}" if par is not None else "",
                        f"{dur:.1f}", int(wait_sec)])
    except Exception as e:
        logging.error(f"Failed to write actions CSV: {e}")

# ================= Scheduler =================
next_ok = {"z1": 0.0, "z3": 0.0}  # both zones active; to disable set to float("inf")
state_pump = False
last_valve_closed_t = 0.0

def run_mist(zone_name: str, valve_dev, plant_vpd: float, par: float):
    global state_pump, last_valve_closed_t
    dur  = pick_mist_duration(plant_vpd)
    wait = pick_wait_interval(par)
    if dur is None or wait is None:
        logging.info(f"{zone_name}: skip (PlantVPD={plant_vpd}, PAR={par}); reschedule")
        next_ok[zone_name] = time.monotonic() + (wait if wait else 5*60)
        return

    logging.info(f"{zone_name}: MIST start — PlantVPD={plant_vpd:.2f}, PAR={par:.1f}, dur={dur}s, next_wait={int(wait/60)}m")

    # Open valve first
    dev_set(valve_dev, f"{zone_name.upper()}_VALVE", True)
    time.sleep(VALVE_LEAD_SEC)

    # Then pump on
    if not state_pump:
        dev_set(pump, "PUMP", True)
        state_pump = True

    # Continue misting for the duration (minus the lead already elapsed)
    time.sleep(max(0.0, dur - VALVE_LEAD_SEC))

    # Close valve and pump together
    dev_set(valve_dev, f"{zone_name.upper()}_VALVE", False)
    last_valve_closed_t = time.monotonic()
    if state_pump:
        dev_set(pump, "PUMP", False)
        state_pump = False

    log_action(zone_name, plant_vpd, par, dur, wait)
    next_ok[zone_name] = time.monotonic() + wait
    logging.info(f"{zone_name}: MIST end — next eligible in {int(wait/60)} min")

# ================= Main loop =================
try:
    while True:
        now_mono = time.monotonic()
        now_local = datetime.now(KSA_TZ)

        z1_ready = now_mono >= next_ok["z1"]
        z3_ready = now_mono >= next_ok["z3"]

        to_try = []
        if z1_ready: to_try.append(("z1", CSV_Z1, z1))
        if z3_ready: to_try.append(("z3", CSV_Z3, z3))

        for name, csv_path, dev in to_try:
            plant_vpd, par, t_air, rh, ts = read_latest_avg(csv_path)

            # freshness + time window + guardrails
            if not fresh(ts):
                logging.info(f"{name}: data stale; retry in 5 min")
                next_ok[name] = now_mono + 5*60
                continue

            if not within_time_window(now_local):
                logging.info(f"{name}: outside time window; retry in 5 min")
                next_ok[name] = now_mono + 5*60
                continue

            if not guardrails_ok(par, t_air, rh):
                logging.info(f"{name}: guardrails failed (PAR={par}, T={t_air}, RH={rh}); retry in 5 min")
                next_ok[name] = now_mono + 5*60
                continue

            run_mist(name, dev, plant_vpd, par)
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
