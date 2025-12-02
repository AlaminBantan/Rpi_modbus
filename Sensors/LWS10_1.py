import minimalmodbus
from time import sleep

LW_1 = minimalmodbus.Instrument('/dev/ttyUSB0', 1)

LW_1.serial.baudrate = 9600
LW_1.serial.bytesize = 8
LW_1.serial.parity   = minimalmodbus.serial.PARITY_NONE
LW_1.serial.stopbits = 1
LW_1.serial.timeout  = 0.5
LW_1.mode = minimalmodbus.MODE_RTU

LW_1.clear_buffers_before_each_transaction = True
LW_1.close_port_after_each_call = True

try:
    while True:
        # Temperature (°C)
        temp_c = LW_1.read_register(
            0,
            number_of_decimals=2,
            functioncode=3,
            signed=True
        )

        # Wetness (%)
        wetness = LW_1.read_register(
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
    LW_1.serial.close()
    print("Ports Now Closed")
