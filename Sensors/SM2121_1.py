import minimalmodbus
from time import sleep

# Create instrument: port + slave address (default is 1)
PH_1 = minimalmodbus.Instrument('/dev/ttyUSB0', 1)

# Serial settings: default for SM2121B
PH_1.serial.baudrate = 9600
PH_1.serial.bytesize = 8
PH_1.serial.parity   = minimalmodbus.serial.PARITY_NONE
PH_1.serial.stopbits = 1
PH_1.serial.timeout  = 0.5
PH_1.mode = minimalmodbus.MODE_RTU

# Good practice
PH_1.clear_buffers_before_each_transaction = True
PH_1.close_port_after_each_call = True

try:
    while True:
        # Read raw pH (register 0 == Modbus 40001), function code 3
        ph_raw = PH_1.read_register(0, 0, functioncode=3, signed=False)

        # Sensor uses scaling of 100 → real pH = raw / 100
        ph_value = ph_raw / 100.0

        print("\n" * 5)
        print("pH Sensor Data-------------------------")
        print(f"Raw value: {ph_raw}")
        print(f"pH:        {ph_value:.2f}")
        print("--------------------------------------")

        sleep(1)

except KeyboardInterrupt:
    PH_1.serial.close()
    print("Ports Now Closed")
