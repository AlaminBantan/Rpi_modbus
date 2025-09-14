#!/usr/bin/env python3
import os, csv, math, statistics, logging
from time import sleep, monotonic
from datetime import datetime, timezone

# ====== InfluxDB 2.x / Cloud settings ======
INFLUX_URL    = "https://us-east-1-1.aws.cloud2.influxdata.com"
INFLUX_TOKEN  = "-Jhy0yP-3X3KBpvpxLXqlDDCa80BO69IOog93VaHRnQyQjGRgLOzGLI1ZwuOJrMJmifxez1f-RVEdNzO9Nvz8g=="
INFLUX_ORG    = "Mishkat greenhouse"
INFLUX_BUCKET = "Mishkat_experiment"


# ====== Files & serial ======
CSV_DIR = "/home/cdacea/climate"
CSV1 = os.path.join(CSV_DIR, "Zone1_minute.csv")
CSV3 = os.path.join(CSV_DIR, "Zone3_minute.csv")
SERIAL_PORT = "/dev/ttyACM0"   # adjust if different
LOG_FILE = os.path.join(CSV_DIR, "Zone_logger.log")

# ====== Logging ======
os.makedirs(CSV_DIR, exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")
logging.info("🌱 Logger start (CSV + optional Influx)")

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

# ====== Setup CSV headers ======
base = ["PAR","Temp","RH","CO2","Pressure","VPD","DewPoint","FanRPM"]
hdr1 = (["datetime"] + [f"{n}_1" for n in base] + [f"{n}_2" for n in base] +
        [f"{n}_3" for n in base] + [f"{n}_avg" for n in base])
hdr3 = (["datetime"] + [f"{n}_4" for n in base] + [f"{n}_5" for n in base] +
        [f"{n}_6" for n in base] + [f"{n}_avg" for n in base])

write_hdr1 = not os.path.exists(CSV1) or os.path.getsize(CSV1) == 0
write_hdr3 = not os.path.exists(CSV3) or os.path.getsize(CSV3) == 0

# ====== Instruments ======
SM_600_1 = make_instrument(1); SM_600_2 = make_instrument(2); SM_600_3 = make_instrument(3)
SM_600_4 = make_instrument(4); SM_600_5 = make_instrument(5); SM_600_6 = make_instrument(6)

# ====== Influx writer ======
def write_influx(zone: str, sensor_label: str, names, values, ts_dt):
    if not influx_enabled: return
    try:
        p = Point("climate").tag("zone", zone).tag("sensor", sensor_label).time(ts_dt)
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
            ts_dt = datetime.now(timezone.utc).replace(microsecond=0)
            ts_csv = ts_dt.isoformat()

            # ---- Zone 1: sensors 1,2,3 (1s spacing) ----
            s1 = read_sensor(SM_600_1); sleep(1)
            s2 = read_sensor(SM_600_2); sleep(1)
            s3 = read_sensor(SM_600_3)

            avg1 = [fmean_ignore_nan([s1[i], s2[i], s3[i]]) for i in range(len(base))]
            row1 = [ts_csv] + [fmt2(v) for v in s1] + [fmt2(v) for v in s2] + [fmt2(v) for v in s3] + [fmt2(v) for v in avg1]
            w1.writerow(row1); f1.flush()

            # Influx (comment out individual sensors if you only want averages)
            write_influx("1", "1",   base, s1,   ts_dt)
            write_influx("1", "2",   base, s2,   ts_dt)
            write_influx("1", "3",   base, s3,   ts_dt)
            write_influx("1", "avg", base, avg1, ts_dt)

            # ---- Zone 3: sensors 4,5,6 (1s spacing) ----
            s4 = read_sensor(SM_600_4); sleep(1)
            s5 = read_sensor(SM_600_5); sleep(1)
            s6 = read_sensor(SM_600_6)

            avg3 = [fmean_ignore_nan([s4[i], s5[i], s6[i]]) for i in range(len(base))]
            row3 = [ts_csv] + [fmt2(v) for v in s4] + [fmt2(v) for v in s5] + [fmt2(v) for v in s6] + [fmt2(v) for v in avg3]
            w3.writerow(row3); f3.flush()

            write_influx("3", "4",   base, s4,   ts_dt)
            write_influx("3", "5",   base, s5,   ts_dt)
            write_influx("3", "6",   base, s6,   ts_dt)
            write_influx("3", "avg", base, avg3, ts_dt)

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
