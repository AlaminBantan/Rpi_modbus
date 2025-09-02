import minimalmodbus
from time import sleep

# --- Helper function to make instruments ---
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

# --- Create 3 instruments ---
SM_600_1 = make_instrument(1)
SM_600_2 = make_instrument(2)
SM_600_3 = make_instrument(3)

# --- Function to read all registers from one sensor ---
def read_sensor(sensor, name):
    try:
        par       = sensor.read_float(0, 3, 2, 0)
        temp_c    = sensor.read_float(2, 3, 2, 0)
        rh_pct    = sensor.read_float(4, 3, 2, 0)
        co2_ppm   = sensor.read_float(6, 3, 2, 0)
        pressure  = sensor.read_float(8, 3, 2, 0)
        vpd_kpa   = sensor.read_float(10, 3, 2, 0)
        dewpoint  = sensor.read_float(12, 3, 2, 0)
        fanrpm    = sensor.read_float(14, 3, 2, 0)

        print("\n" * 5)
        print(f"{name} Sensor Data-------------------------------")
        print(f"PAR         : {par:.2f} µmol m^-2 s^-1")
        print(f"Temperature : {temp_c:.2f} °C")
        print(f"RH          : {rh_pct:.2f} %")
        print(f"CO₂         : {co2_ppm:.2f} ppm")
        print(f"Pressure    : {pressure:.2f} kPa")
        print(f"VPD         : {vpd_kpa:.3f} kPa")
        print(f"Dew Point   : {dewpoint:.2f} °C")
        print(f"Fan RPM     : {fanrpm:.2f} rpm")
        print("-----------------------------------------------")

    except Exception as e:
        print(f"⚠️ Error reading {name}: {e}")

# --- Main loop ---
try:
    while True:
        read_sensor(SM_600_1, "SM-600_1")
        sleep(1)   # wait 1 second before next sensor
        read_sensor(SM_600_2, "SM-600_2")
        sleep(1)   # wait 1 second before next sensor
        read_sensor(SM_600_3, "SM-600_3")
        sleep(5)   # wait 5 seconds before repeating

except KeyboardInterrupt:
    print("✅ Stopped. Ports Now Closed.")
    try:
        SM_600_1.serial.close()
        SM_600_2.serial.close()
        SM_600_3.serial.close()
    except:
        pass
