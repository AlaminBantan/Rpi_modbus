import minimalmodbus  # Don't forget to import the library!!
from time import sleep

# Make an "instrument" object called carbo_211 (port name, slave address (in decimal))
carbo_211 = minimalmodbus.Instrument('/dev/ttyACM0', 211, debug=False)

# Serial config
carbo_211.serial.baudrate = 19200
carbo_211.serial.bytesize = 8
carbo_211.serial.parity = minimalmodbus.serial.PARITY_NONE
carbo_211.serial.stopbits = 1
carbo_211.serial.timeout = 1.0  # optional: helps avoid hangs

carbo_211.mode = minimalmodbus.MODE_RTU

# Good practice to clean up before and after each execution
carbo_211.clear_buffers_before_each_transaction = True
carbo_211.close_port_after_each_call = True

# Register map (addresses in hex for clarity; Python treats them as ints)
REG_CO2_AVG = 0x424  # 1060 decimal
REG_CO2_RAW = 0x426  # 1062 decimal

try:
    while True:
        # read_float(registeraddress, functioncode=3, number_of_registers=2, byteorder=0)
        # Use functioncode=4 for Input Registers
        co2_avg = carbo_211.read_float(REG_CO2_AVG, functioncode=4, number_of_registers=2, byteorder=0)
        co2_raw = carbo_211.read_float(REG_CO2_RAW, functioncode=4, number_of_registers=2, byteorder=0)

        print("\n" * 50)
        print("Sensor Data--------------------------------")
        print(f"CO2 AVG (0x{REG_CO2_AVG:X}): {co2_avg} ppm")
        print(f"CO2 RAW (0x{REG_CO2_RAW:X}): {co2_raw} ppm")
        print("------------------------------------------")
        sleep(10)

except KeyboardInterrupt:
    carbo_211.serial.close()
    print("Ports Now Closed")
