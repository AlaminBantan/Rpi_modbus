import minimalmodbus
from time import sleep

LW_10 = minimalmodbus.Instrument('/dev/ttyUSB0', 10)

LW_10.serial.baudrate = 19200
LW_10.serial.bytesize = 8
LW_10.serial.parity   = minimalmodbus.serial.PARITY_EVEN
LW_10.serial.stopbits = 1
LW_10.serial.timeout  = 0.5
LW_10.mode = minimalmodbus.MODE_RTU

LW_10.clear_buffers_before_each_transaction = True
LW_10.close_port_after_each_call = True

try:
    while True:
        # Temperature (°C)
        temp_c = LW_10.read_register(
            0,
            number_of_decimals=2,
            functioncode=3,
            signed=True
        )

        # Wetness (%)
        wetness = LW_10.read_register(
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
    LW_10.serial.close()
    print("Ports Now Closed")
