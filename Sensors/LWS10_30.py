import minimalmodbus
from time import sleep

LW_30 = minimalmodbus.Instrument('/dev/ttyUSB0', 30)

LW_30.serial.baudrate = 19200
LW_30.serial.bytesize = 8
LW_30.serial.parity   = minimalmodbus.serial.PARITY_EVEN
LW_30.serial.stopbits = 1
LW_30.serial.timeout  = 0.5
LW_30.mode = minimalmodbus.MODE_RTU

LW_30.clear_buffers_before_each_transaction = True
LW_30.close_port_after_each_call = True

try:
    while True:
        # Temperature (°C)
        temp_c = LW_30.read_register(
            0,
            number_of_decimals=2,
            functioncode=3,
            signed=True
        )

        # Wetness (%)
        wetness = LW_30.read_register(
            1,
            number_of_decimals=2,
            functioncode=3,
            signed=False
        )

        print("\n" * 50)
        print("Sensor Data--------------------------------")
        print(f"Temperature: {temp_c:.2f} °C")
        print(f"Wetness:     {wetness:.2f} %")
        print("------------------------------------------")
        sleep(1)

except KeyboardInterrupt:
    LW_30.serial.close()
    print("Ports Now Closed")
