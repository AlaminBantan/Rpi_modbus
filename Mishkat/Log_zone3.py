import minimalmodbus
from time import sleep, monotonic
from datetime import datetime
import csv
import os
import math
import statistics

CSV_DIR = "/home/cdacea/climate"
CSV_PATH = os.path.join(CSV_DIR, "Zone3_minute.csv")   # <-- Zone3 file

# --- Helper to build instruments ---
def make_instrument(address):
    instr = minimalmodbus.Instrument('/dev/ttyACM0', address, debug=False)
    instr.serial.baudrate = 19200
    instr.serial.bytesize = 8
    instr.serial.parity = minimalmodbus.serial.PARITY_EVEN
    instr.serial.stopbits = 1
    instr.mode = minimalmodbus.MODE_RTU
    instr.clear_buffers_before_each_transaction = True
    instr.close_port_after_each_call = True
    return instr

# --- Create instruments (Zone3 sensors: 4, 5, 6) ---
SM_600_4 = make_instrument(4)
SM_600_5 = make_instrument(5)
SM_600_6 = make_instrument(6)

# --- Read all registers from one sensor; return tuple of 8 values ---
def read_sensor(sensor):
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
        print(f"⚠️ Read error ({sensor.address}): {e}")
        nan8 = (math.nan,)*8
        return nan8

# --- Ensure directory and header ---
os.makedirs(CSV_DIR, exist_ok=True)
base_names = ["PAR","Temp","RH","CO2","Pressure","VPD","DewPoint","FanRPM"]

header = (
    ["datetime"] +
    [f"{name}_4" for name in base_names] +
    [f"{name}_5" for name in base_names] +
    [f"{name}_6" for name in base_names] +
    [f"{name}_avg" for name in base_names]   # average columns
)

write_header = not os.path.exists(CSV_PATH) or os.path.getsize(CSV_PATH) == 0

# --- Main loop: one row per minute ---
try:
    with open(CSV_PATH, "a", newline="") as f:
        writer = csv.writer(f)

        if write_header:
            writer.writerow(header)
            f.flush()

        while True:
            loop_start = monotonic()

            ts = datetime.now().isoformat(timespec="seconds")

            # Read three sensors 1s apart
            s4 = read_sensor(SM_600_4)
            sleep(1)
            s5 = read_sensor(SM_600_5)
            sleep(1)
            s6 = read_sensor(SM_600_6)

            # Compute averages (ignores NaN if possible)
            averages = []
            for idx in range(len(base_names)):
                values = [s4[idx], s5[idx], s6[idx]]
                try:
                    avg_val = statistics.fmean(v for v in values if not math.isnan(v))
                except Exception:
                    avg_val = math.nan
                averages.append(avg_val)

            # Format all numbers to 2 decimals (strings for CSV)
            def fmt(x):
                return f"{x:.2f}" if not math.isnan(x) else ""

            row = [ts] + [fmt(v) for v in s4] + [fmt(v) for v in s5] + [fmt(v) for v in s6] + [fmt(v) for v in averages]
            writer.writerow(row)
            f.flush()

            # Keep a steady 60s cadence
            elapsed = monotonic() - loop_start
            sleep_time = max(0.0, 60.0 - elapsed)
            sleep(sleep_time)

except KeyboardInterrupt:
    print("✅ Logging stopped. Ports now closing.")
    try:
        SM_600_4.serial.close()
        SM_600_5.serial.close()
        SM_600_6.serial.close()
    except:
        pass
