import minimalmodbus
from time import sleep, monotonic
from datetime import datetime
import csv
import os
import math
import statistics

CSV_DIR = "/home/cdacea/climate"
CSV1 = os.path.join(CSV_DIR, "Zone1_minute.csv")
CSV3 = os.path.join(CSV_DIR, "Zone3_minute.csv")
SERIAL_PORT = "/dev/ttyACM0"  # adjust if needed

# ------------------- Helpers -------------------
def make_instrument(address):
    instr = minimalmodbus.Instrument(SERIAL_PORT, address, debug=False)
    instr.serial.baudrate = 19200
    instr.serial.bytesize = 8
    instr.serial.parity = minimalmodbus.serial.PARITY_EVEN
    instr.serial.stopbits = 1
    instr.mode = minimalmodbus.MODE_RTU
    instr.clear_buffers_before_each_transaction = True
    instr.close_port_after_each_call = True
    return instr

def read_sensor(sensor):
    """Read one SM-600: returns 8-tuple or NaNs on error."""
    try:
        par       = sensor.read_float(0, 3, 2, 0)
        temp_c    = sensor.read_float(2, 3, 2, 0)
        rh_pct    = sensor.read_float(4, 3, 2, 0)
        co2_ppm   = sensor.read_float(6, 3, 2, 0)
        pressure  = sensor.read_float(8, 3, 2, 0)
        vpd_kpa   = sensor.read_float(10, 3, 2, 0)
        dewpoint  = sensor.read_float(12, 3, 2, 0)
        fanrpm    = sensor.read_float(14, 3, 2, 0)
        return (par, temp_c, rh_pct, co2_ppm, pressure, vpd_kpa, dewpoint, fanrpm)
    except Exception as e:
        try:
            addr = sensor.address
        except Exception:
            addr = "?"
        print(f"⚠️ Read error (addr {addr}): {e}")
        return (math.nan,)*8

def fmean_ignore_nan(values):
    vals = [v for v in values if not math.isnan(v)]
    return statistics.fmean(vals) if vals else math.nan

def fmt2(x):
    return f"{x:.2f}" if not math.isnan(x) else ""

# ------------------- Setup -------------------
os.makedirs(CSV_DIR, exist_ok=True)
base = ["PAR","Temp","RH","CO2","Pressure","VPD","DewPoint","FanRPM"]

hdr_zone1 = (["datetime"] +
             [f"{n}_1" for n in base] +
             [f"{n}_2" for n in base] +
             [f"{n}_3" for n in base] +
             [f"{n}_avg" for n in base])

hdr_zone3 = (["datetime"] +
             [f"{n}_4" for n in base] +
             [f"{n}_5" for n in base] +
             [f"{n}_6" for n in base] +
             [f"{n}_avg" for n in base])

write_hdr1 = not os.path.exists(CSV1) or os.path.getsize(CSV1) == 0
write_hdr3 = not os.path.exists(CSV3) or os.path.getsize(CSV3) == 0

# Instruments
SM_600_1 = make_instrument(1)
SM_600_2 = make_instrument(2)
SM_600_3 = make_instrument(3)
SM_600_4 = make_instrument(4)
SM_600_5 = make_instrument(5)
SM_600_6 = make_instrument(6)

# ------------------- Main loop -------------------
try:
    with open(CSV1, "a", newline="") as f1, open(CSV3, "a", newline="") as f3:
        w1 = csv.writer(f1)
        w3 = csv.writer(f3)

        if write_hdr1:
            w1.writerow(hdr_zone1); f1.flush()
        if write_hdr3:
            w3.writerow(hdr_zone3); f3.flush()

        while True:
            loop_start = monotonic()
            ts = datetime.now().isoformat(timespec="seconds")

            # --- Zone 1: sensors 1,2,3 (1s spacing) ---
            s1 = read_sensor(SM_600_1); sleep(1)
            s2 = read_sensor(SM_600_2); sleep(1)
            s3 = read_sensor(SM_600_3)

            avg1 = [fmean_ignore_nan([s1[i], s2[i], s3[i]]) for i in range(len(base))]
            row1 = [ts] + [fmt2(v) for v in s1] + [fmt2(v) for v in s2] + [fmt2(v) for v in s3] + [fmt2(v) for v in avg1]
            w1.writerow(row1); f1.flush()

            # --- Zone 3: sensors 4,5,6 (1s spacing) ---
            s4 = read_sensor(SM_600_4); sleep(1)
            s5 = read_sensor(SM_600_5); sleep(1)
            s6 = read_sensor(SM_600_6)

            avg3 = [fmean_ignore_nan([s4[i], s5[i], s6[i]]) for i in range(len(base))]
            row3 = [ts] + [fmt2(v) for v in s4] + [fmt2(v) for v in s5] + [fmt2(v) for v in s6] + [fmt2(v) for v in avg3]
            w3.writerow(row3); f3.flush()

            # Keep a steady 60s cadence from start of loop
            elapsed = monotonic() - loop_start
            sleep(max(0.0, 60.0 - elapsed))

except KeyboardInterrupt:
    print("✅ Logging stopped. Ports now closing.")
    for inst in (SM_600_1, SM_600_2, SM_600_3, SM_600_4, SM_600_5, SM_600_6):
        try:
            inst.serial.close()
        except Exception:
            pass
