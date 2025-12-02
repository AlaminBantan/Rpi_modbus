import minimalmodbus
from time import sleep

PH_1 = minimalmodbus.Instrument('/dev/ttyUSB0', 21)  # new address

PH_1.serial.baudrate = 19200          # matches what you set above
PH_1.serial.bytesize = 8
PH_1.serial.parity   = minimalmodbus.serial.PARITY_NONE  # cannot change to EVEN
PH_1.serial.stopbits = 1
PH_1.serial.timeout  = 0.5
PH_1.mode = minimalmodbus.MODE_RTU

PH_1.clear_buffers_before_each_transaction = True
PH_1.close_port_after_each_call = True

try:
    while True:
        # pH at register 0 (40001), scaled x100
        ph_raw = PH_1.read_register(0, 0, functioncode=3, signed=False)
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
