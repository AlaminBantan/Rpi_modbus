#!/usr/bin/env python3
import os, csv, math, statistics, logging
from time import sleep, monotonic
from datetime import datetime, timezone
from zoneinfo import ZoneInfo  # Python 3.9+

# ====== InfluxDB 2.x / Cloud settings ======
INFLUX_URL    = "https://us-east-1-1.aws.cloud2.influxdata.com"  # your cluster URL
INFLUX_TOKEN  = ""            # <-- paste your API token (leave empty to disable Influx writes)
INFLUX_ORG    = "Mishkat greenhouse"
INFLUX_BUCKET = "Mishkat_experiment"

# ====== Files & serial ======
CSV_DIR = "/home/cdacea/climate"
CSV1 = os.path.join(CSV_DIR, "Zone1_minute.csv")
CSV3 = os.path.join(CSV_DIR, "Zone3_minute.csv")
SERIAL_PORT = "/dev/ttyACM0"   # adjust if different
LOG_FILE = os.path.join(CSV_DIR, "Zone_logger.log")

# ====== Timezones ======
ksa = ZoneInfo("Asia/Riyadh")  # for CSV local time

# ====== Logging ======
os.makedirs(CSV_DIR, exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")
logging.info("🌱 Logger start (CSV local + Influx UTC)")

# ====== Influx client (optional) ======
influx_enabled = bool(INFLUX_TOKEN.strip())
if influx_enabled:
    try:
        from influxdb_client import InfluxDBClient, Point, WriteOptions
        influx = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG, timeout=30_000)
        write_api = influx.write_api(write_options=WriteOptions(batch_size=500, flush_interval=1_000))
        logging.info("✅ Influx client ready")
    except Exception as e:
        influx_enabled = False
        logging.error(f"❌ Influx init failed; continuing without Influx: {e}")

# ====== Modbus helpers ======
import minimalmodbus
def make_instrument(address: int):
    instr = minimalmodbus.Instrument(SERIAL_PORT, address, debug=False)
    # Robust serial settings
    instr.serial.baudrate = 19200           # try 9600 if your bus is noisy
    instr.serial.timeout = 0.4
    instr.serial.write_timeout = 0.4
    instr.serial.inter_byte_timeout = 0.05
    instr.serial.bytesize = 8
    instr.serial.parity = minimalmodbus.serial.PARITY_EVEN
    instr.serial.stopbits = 1
    instr.mode = minimalmodbus.MODE_RTU
    instr.clear_buffers_before_each_transaction = True
    instr.close_port_after_each_call = True
    instr.handle_local_echo = False
    return instr

def read_float_retry(instr, reg, tries=3, delay=0.1):
    for k in range(tries):
        try:
            return instr.read_float(reg, functioncode=3, number_of_registers=2, byteorder=0)  # big-endian
        except Exception as e:
            if k == tries - 1:
                logging.error(f"Read failed addr {instr.address} reg {reg}: {e}")
                return math.nan
            sleep(delay)

def read_sensor(instr):
    # Returns tuple of 8 values or NaNs: PAR, Temp, RH, CO2, Pressure, VPD, DewPoint, FanRPM
    return (
        read_float_retry(instr, 0),
        read_float_retry(instr, 2),
        read_float_retry(instr, 4),
        read_float_retry(instr, 6),
        read_float_retry(instr, 8),
        read_float_retry(instr,10),
        read_float_retry(instr,12),
        read_float_retry(instr,14),
    )

def fmean_ignore_nan(values):
    vals = [v for v in values if not math.isnan(v)]
    return statistics.fmean(vals) if vals else math.nan

def fmt2(x):
    return f"{x:.2f}" if not math.isnan(x) else ""

# ====== Plant VPD helpers ======
def esat_kpa(Tc: float) -> float:
    """Saturation vapor pressure (kPa) at temperature Tc (°C). Tetens formula."""
    return 0.6108 * math.exp((17.27 * Tc) / (Tc + 237.3))

def plant_vpd_kpa(air_Tc: float, RH_pct: float, leaf_Tc: float) -> float:
    """
    VPD_leaf = es(T_leaf) - ea_air, where ea_air = RH * es(T_air) / 100.
    Clamp at >= 0.
    """
    if any(math.isnan(v) for v in (air_Tc, RH_pct, leaf_Tc)):
        return math.nan
    ea_air = (RH_pct / 100.0) * esat_kpa(air_Tc)
    vpd = esat_kpa(leaf_Tc) - ea_air
    return max(0.0, vpd)

# ====== Setup CSV headers ======
base = ["PAR","Temp","RH","CO2","Pressure","VPD","DewPoint","FanRPM"]
# We will append two extra *avg* columns: PlantTemp_avg, PlantVPD_avg
hdr1 = (["datetime"] + [f"{n}_1" for n in base] + [f"{n}_2" for n in base] +
        [f"{n}_3" for n in base] + [f"{n}_avg" for n in base] + ["PlantTemp_avg","PlantVPD_avg"])
hdr3 = (["datetime"] + [f"{n}_4" for n in base] + [f"{n}_5" for n in base] +
        [f"{n}_6" for n in base] + [f"{n}_avg" for n in base] + ["PlantTemp_avg","PlantVPD_avg"])

write_hdr1 = not os.path.exists(CSV1) or os.path.getsize(CSV1) == 0
write_hdr3 = not os.path.exists(CSV3) or os.path.getsize(CSV3) == 0

# ====== Instruments ======
SM_600_1 = make_instrument(1); SM_600_2 = make_instrument(2); SM_600_3 = make_instrument(3)
SM_600_4 = make_instrument(4); SM_600_5 = make_instrument(5); SM_600_6 = make_instrument(6)

# ====== Influx writer ======
def write_influx(zone: str, sensor_label: str, names, values, ts_dt_utc):
    if not influx_enabled: return
    try:
        p = Point("climate").tag("zone", zone).tag("sensor", sensor_label).time(ts_dt_utc)
        for n, v in zip(names, values):
            if not math.isnan(v):
                p.field(n, round(float(v), 2))
        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=p)
    except Exception as e:
        logging.error(f"Influx write failed (zone {zone} sensor {sensor_label}): {e}")

# ====== Main loop ======
try:
    with open(CSV1, "a", newline="") as f1, open(CSV3, "a", newline="") as f3:
        w1 = csv.writer(f1); w3 = csv.writer(f3)
        if write_hdr1: w1.writerow(hdr1); f1.flush()
        if write_hdr3: w3.writerow(hdr3); f3.flush()

        while True:
            loop_start = monotonic()

            # --- timestamps ---
            ts_dt_utc   = datetime.now(timezone.utc).replace(microsecond=0)  # for Influx
            ts_dt_local = datetime.now(ksa).replace(microsecond=0)           # for CSV
            ts_csv      = ts_dt_local.isoformat()                            # e.g., ...+03:00

            # ---- Zone 1: sensors 1,2,3 (1s spacing) ----
            s1 = read_sensor(SM_600_1); sleep(1)
            s2 = read_sensor(SM_600_2); sleep(1)
            s3 = read_sensor(SM_600_3)

            # avg1 over the 8 base vars
            avg1 = [fmean_ignore_nan([s1[i], s2[i], s3[i]]) for i in range(len(base))]
            PAR1, Tair1, RH1, CO21, P1, VPD1, Dew1, Fan1 = avg1

            # plant metrics (avg): T_leaf = T_air - 2 C; VPD_leaf = es(T_leaf) - RH*es(T_air)
            plantT1 = Tair1 - 2.0 if not math.isnan(Tair1) else math.nan
            plantVPD1 = plant_vpd_kpa(Tair1, RH1, plantT1)

            row1 = (
                [ts_csv]
                + [fmt2(v) for v in s1] + [fmt2(v) for v in s2] + [fmt2(v) for v in s3]
                + [fmt2(v) for v in avg1] + [fmt2(plantT1), fmt2(plantVPD1)]
            )
            w1.writerow(row1); f1.flush()

            # Influx (individual sensors unchanged)
            write_influx("1", "1",   base, s1,   ts_dt_utc)
            write_influx("1", "2",   base, s2,   ts_dt_utc)
            write_influx("1", "3",   base, s3,   ts_dt_utc)
            # avg + plant metrics
            names_avg1  = base + ["PlantTemp","PlantVPD"]
            values_avg1 = avg1 + [plantT1, plantVPD1]
            write_influx("1", "avg", names_avg1, values_avg1, ts_dt_utc)

            # ---- Zone 3: sensors 4,5,6 (1s spacing) ----
            s4 = read_sensor(SM_600_4); sleep(1)
            s5 = read_sensor(SM_600_5); sleep(1)
            s6 = read_sensor(SM_600_6)

            avg3 = [fmean_ignore_nan([s4[i], s5[i], s6[i]]) for i in range(len(base))]
            PAR3, Tair3, RH3, CO23, P3, VPD3, Dew3, Fan3 = avg3

            plantT3 = Tair3 - 2.0 if not math.isnan(Tair3) else math.nan
            plantVPD3 = plant_vpd_kpa(Tair3, RH3, plantT3)

            row3 = (
                [ts_csv]
                + [fmt2(v) for v in s4] + [fmt2(v) for v in s5] + [fmt2(v) for v in s6]
                + [fmt2(v) for v in avg3] + [fmt2(plantT3), fmt2(plantVPD3)]
            )
            w3.writerow(row3); f3.flush()

            write_influx("3", "4",   base, s4,   ts_dt_utc)
            write_influx("3", "5",   base, s5,   ts_dt_utc)
            write_influx("3", "6",   base, s6,   ts_dt_utc)
            names_avg3  = base + ["PlantTemp","PlantVPD"]
            values_avg3 = avg3 + [plantT3, plantVPD3]
            write_influx("3", "avg", names_avg3, values_avg3, ts_dt_utc)

            # keep a steady 60s cadence
            sleep(max(0.0, 60.0 - (monotonic() - loop_start)))

except KeyboardInterrupt:
    logging.info("🌱 Logger stopped by user.")
finally:
    # Close serial ports politely
    for inst in (SM_600_1, SM_600_2, SM_600_3, SM_600_4, SM_600_5, SM_600_6):
        try:
            inst.serial.close()
        except Exception:
            pass
    if influx_enabled:
        try:
            influx.close()
        except Exception:
            pass
