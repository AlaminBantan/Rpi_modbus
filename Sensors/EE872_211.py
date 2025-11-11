import minimalmodbus
from time import sleep

carbo_211 = minimalmodbus.Instrument('/dev/ttyACM0', 211, debug=False)
carbo_211.serial.baudrate = 19200
carbo_211.serial.bytesize = 8
carbo_211.serial.parity = minimalmodbus.serial.PARITY_NONE
carbo_211.serial.stopbits = 1
carbo_211.serial.timeout = 1.0
carbo_211.mode = minimalmodbus.MODE_RTU
carbo_211.clear_buffers_before_each_transaction = True
carbo_211.close_port_after_each_call = True

REG_CO2_AVG_FLOAT = 0x424  # 1060
REG_CO2_RAW_FLOAT = 0x426  # 1062
REG_CO2_AVG_INT   = 0xFBE  # 4030
REG_CO2_RAW_INT   = 0xFBF  # 4031

BYTEORDER = minimalmodbus.BYTEORDER_BIG_SWAP  # <-- key change for EE872 floats

try:
    while True:
        # Preferred: 32-bit float reads (FC=4 works per manual; FC=3 also OK)
        co2_avg = carbo_211.read_float(REG_CO2_AVG_FLOAT, functioncode=4, number_of_registers=2, byteorder=BYTEORDER)
        co2_raw = carbo_211.read_float(REG_CO2_RAW_FLOAT, functioncode=4, number_of_registers=2, byteorder=BYTEORDER)

        # Optional cross-check: 16-bit integer registers (scale = 1 ppm)
        co2_avg_i = carbo_211.read_register(REG_CO2_AVG_INT, functioncode=4, signed=True)
        co2_raw_i = carbo_211.read_register(REG_CO2_RAW_INT, functioncode=4, signed=True)

        print("\n" * 50)
        print("Sensor Data--------------------------------")
        print(f"CO2 AVG float (0x{REG_CO2_AVG_FLOAT:X}): {co2_avg:.1f} ppm")
        print(f"CO2 RAW  float (0x{REG_CO2_RAW_FLOAT:X}): {co2_raw:.1f} ppm")
        print(f"CO2 AVG int   (0x{REG_CO2_AVG_INT:X}): {co2_avg_i} ppm")
        print(f"CO2 RAW int   (0x{REG_CO2_RAW_INT:X}): {co2_raw_i} ppm")
        print("------------------------------------------")
        sleep(10)

except KeyboardInterrupt:
    carbo_211.serial.close()
    print("Ports Now Closed")
