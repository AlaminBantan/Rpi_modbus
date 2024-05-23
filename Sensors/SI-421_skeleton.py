import serial
import time
import io
import csv
from datetime import datetime

with open('/home/cdacea/IR/infrarednew.csv','a',newline='') as f:
    header = ['time','S0','S1','S2','S3','S4', 'S5']
    write_head = csv.writer(f)
    write_head.writerow(header)
    f.close()
print("Header added")
time.sleep(1)
s_l = [1, 2, 3, 4, 5, 0]
se = serial.Serial("/dev/ttyUSB0",
                baudrate=9600,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                xonxoff=False,
                timeout=1)

sio = io.TextIOWrapper(io.BufferedRWPair(se,se))
while True:
    #s_l = [1, 2, 3, 4, 5, 6]
    data_list = [datetime.now().replace(microsecond=0)]
    for s in s_l:
    #Command is the Slave ID + M!, to take measurement
        command = str(s)+"M!\r"
        sio.write(command)
        sio.flush()
        time.sleep(0.2)
    #read bit

        data_str = str(s)+"D0!\r"
        sio.write(data_str)
        data = sio.readline()
        sio.flush()
        data_list.append(data[2:8])
        time.sleep(0.2)
        #print(s)
        print("measure :",data)

    with open('/home/cdacea/IR/infrarednew.csv','a', newline='') as f:
        print("data list: ", data_list)
        w = csv.writer(f)
        w.writerow(data_list)
        f.close()
#ilhan
    print("row added")
    time.sleep(60)