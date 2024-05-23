import serial
import time
import io

IR_0 = serial.Serial("/dev/ttyUSB0",
                   baudrate=9600,
                   bytesize=serial.EIGHTBITS,
                   parity=serial.PARITY_NONE,
                   stopbits=serial.STOPBITS_ONE,
                   xonxoff=False,
                   timeout=1)
IR_01 = io.TextIOWrapper(io.BufferedRWPair(IR_0, IR_0))
try:
    while True:
        # command_command_5 is the Slave ID + M!, to take measurement
        command_0 = "?!"
        IR_01.write(command_0)
        IR_01.flush()
        time.sleep(1)        
        print("send")
        # read bit
        data_0 = IR_01.readlines()
        IR_01.flush()
        print("read")
        time.sleep(1)
        print(data_0)
        time.sleep(1)
except KeyboardInterrupt:
    # Clean up when interrupted
    print("Ports Now Closed")