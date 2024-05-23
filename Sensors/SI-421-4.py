import serial
import time
import io
import csv
from datetime import datetime

IR_4 = serial.Serial("/dev/ttyACM0",
                   baudrate=9600,
                   bytesize=serial.EIGHTBITS,
                   parity=serial.PARITY_NONE,
                   stopbits=serial.STOPBITS_ONE,
                   xonxoff=False,
                   timeout=1)
IR_4 = io.TextIOWrapper(io.BufferedRWPair(IR_4, IR_4))
try:
    while True:
        # command_4 is the Slave ID + M!, to take measurement
        command_4 = "4M!\r"
        IR_4.write(command_4)
        IR_4.flush()
        time.sleep(1)
        # read bit
        data_str ="4D0!\r"
        IR_4.write(data_str)
        data_4 = IR_4.readline()
        IR_4.flush()
        time.sleep(1)
        if len(data_4.split('+'))> 1:
            print(f"Temperature of the surface 4 is: {data_4.split('+')[1]} degrees celcius")
except KeyboardInterrupt:
    # Clean up when interrupted
    print("Ports Now Closed")