import serial
import time
import io
import csv
from datetime import datetime

IR_2 = serial.Serial("/dev/ttyACM0",
                   baudrate=9600,
                   bytesize=serial.EIGHTBITS,
                   parity=serial.PARITY_NONE,
                   stopbits=serial.STOPBITS_ONE,
                   xonxoff=False,
                   timeout=1)
IR_2 = io.TextIOWrapper(io.BufferedRWPair(IR_2, IR_2))
try:
    while True:
        # command_2 is the Slave ID + M!, to take measurement
        command_2 = "2M!\r"
        IR_2.write(command_2)
        IR_2.flush()
        time.sleep(1)
        # read bit
        data_str_2 ="2D0!\r"
        IR_2.write(data_str_2)
        data_2 = IR_2.readline()
        IR_2.flush()
        time.sleep(1)
        if len(data_2.split('+'))> 1:
            print(f"Temperature of the surface is: {data_2.split('+')[1]} degrees celcius")
except KeyboardInterrupt:
    # Clean up when interrupted
    print("Ports Now Closed")