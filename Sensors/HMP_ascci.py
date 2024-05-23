import serial
import io
from time import sleep
from datetime import datetime

serial_THUM = serial.Serial("/dev/ttyACM1",
                            baudrate=4800,
                            bytesize=serial.SEVENBITS,
                            parity=serial.PARITY_EVEN,
                            stopbits=serial.STOPBITS_ONE,
                            xonxoff=False,
                            timeout=2)

THUM_33 = io.TextIOWrapper(io.BufferedRWPair(serial_THUM, serial_THUM))

try:
    while True:
        THUM_33.write("OPEN 33\r\n")
        THUM_33.flush()
        print("33 is opened")
        sleep(1)

        THUM_33.write("SEND\r\n")
        THUM_33.flush()
        print("send")
        sleep(2)
        
        data_33 = THUM_33.readlines()

        # Extracting RH and Temp from the last line of data
        last_line = data_33[-1]
        rh_index = last_line.find('RH=')
        temp_index = last_line.find("Ta=")

        if rh_index != -1 and temp_index != -1:
            rh_value = float(last_line[rh_index + 3:last_line.find('%RH')])
            temp_value = float(last_line[temp_index + 3:last_line.find("'C")])

            print(f"RH= {rh_value} %RH")
            print(f"Temp= {temp_value} 'C")

        sleep(3)

        THUM_33.write("CLOSE\r\n")
        print("closed")
        sleep(2)

except KeyboardInterrupt:
    # Clean up when interrupted
    print("Ports Now Closed")


