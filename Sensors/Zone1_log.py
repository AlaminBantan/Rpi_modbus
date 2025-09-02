import minimalmodbus
from time import sleep, monotonic
from datetime import datetime
import csv
import os
import math

CSV_DIR = "/home/cdacea/climate"
CSV_PATH = os.path.join(CSV_DIR, "Zone1_minute.csv")

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

# --- Create instruments ---
SM_600_1 = make_instrument(1)
SM_600_2 = make_instrument(2)
SM_600_3 = make_instrument(3)

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
        # Use NaNs to keep CSV shape consistent
        nan8 = (math.nan,)*8
        return nan8

# --- Ensure directory and header ---
os.makedirs(CSV_DIR, exist_ok=True)
header = (
    ["datetime"] +
    [f"{name}_1" for name in ["PAR","Temp","RH","CO2","Pressure","VPD","DewPoint","FanRPM"]] +
    [f"{name}_2" for name in ["PAR","Temp","RH","CO2","Pressure","VPD","DewPoint","FanRPM"]] +
    [f"{name}_3" for name in ["PAR","Temp","RH","CO2","Pressure","VPD","DewPoint","FanRPM"]]
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

            # Timestamp
            ts = datetime.now().isoformat(timespec="seconds")

            # Read sensors 1s apart to give the bus some breathing room
            s1 = read_sensor(SM_600_1)
            sleep(1)
            s2 = read_sensor(SM_600_2)
            sleep(1)
            s3 = read_sensor(SM_600_3)

            row = [ts] + list(s1) + list(s2) + list(s3)
            writer.writerow(row)
            f.flush()

            # Keep a steady 60s cadence from the loop start
            elapsed = monotonic() - loop_start
            sleep_time = max(0.0, 60.0 - elapsed)
            sleep(sleep_time)

except KeyboardInterrupt:
    print("✅ Logging stopped. Ports now closing.")
    try:
        SM_600_1.serial.close()
        SM_600_2.serial.close()
        SM_600_3.serial.close()
    except:
        pass
