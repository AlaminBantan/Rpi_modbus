import serial
import time
import io
import csv
from datetime import datetime

IR_5 = serial.Serial("/dev/ttyACM0",
                   baudrate=9600,
                   bytesize=serial.EIGHTBITS,
                   parity=serial.PARITY_NONE,
                   stopbits=serial.STOPBITS_ONE,
                   xonxoff=False,
                   timeout=1)
IR_5 = io.TextIOWrapper(io.BufferedRWPair(IR_5, IR_5))
try:
    while True:
        # command_5 is the Slave ID + M!, to take measurement
        command_5 = "5M!\r"
        IR_5.write(command_5)
        IR_5.flush()
        time.sleep(1)
        # read bit
        data_str ="5D0!\r"
        IR_5.write(data_str)
        data_5 = IR_5.readline()
        IR_5.flush()
        time.sleep(1)
        if len(data_5.split('+'))> 1:
            print(f"Temperature of the surface 5 is: {data_5.split('+')[1]} degrees celcius")
except KeyboardInterrupt:
    # Clean up when interrupted
    print("Ports Now Closed")