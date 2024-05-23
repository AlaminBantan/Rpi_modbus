from time import sleep
import datetime
import csv
import serial
import time
import io


#configuration of SI-421 ID=1
IR_1 = serial.Serial("/dev/ttyACM0",
                   baudrate=9600,
                   bytesize=serial.EIGHTBITS,
                   parity=serial.PARITY_NONE,
                   stopbits=serial.STOPBITS_ONE,
                   xonxoff=False,
                   timeout=1)
IR_1 = io.TextIOWrapper(io.BufferedRWPair(IR_1, IR_1))

#configuration of SI-421 ID=2
IR_2 = serial.Serial("/dev/ttyACM0",
                   baudrate=9600,
                   bytesize=serial.EIGHTBITS,
                   parity=serial.PARITY_NONE,
                   stopbits=serial.STOPBITS_ONE,
                   xonxoff=False,
                   timeout=1)
IR_2 = io.TextIOWrapper(io.BufferedRWPair(IR_2, IR_2))

#configuration of SI-421 ID=3
IR_3 = serial.Serial("/dev/ttyACM0",
                   baudrate=9600,
                   bytesize=serial.EIGHTBITS,
                   parity=serial.PARITY_NONE,
                   stopbits=serial.STOPBITS_ONE,
                   xonxoff=False,
                   timeout=1)
IR_3 = io.TextIOWrapper(io.BufferedRWPair(IR_3, IR_3))

#configuration of SI-421 ID=4
IR_4 = serial.Serial("/dev/ttyACM0",
                   baudrate=9600,
                   bytesize=serial.EIGHTBITS,
                   parity=serial.PARITY_NONE,
                   stopbits=serial.STOPBITS_ONE,
                   xonxoff=False,
                   timeout=1)
IR_4 = io.TextIOWrapper(io.BufferedRWPair(IR_4, IR_4))




# Define a function to get the current date and time in the required format
def get_datetime():
    now = datetime.datetime.now()
    return now.strftime("%m/%d/%Y"), now.strftime("%H:%M")

# Define the file path for the CSV file
IR_csv_file_path = "/home/cdacea/GH_data/IR.csv"

try:
    with open(IR_csv_file_path, mode='a', newline='') as csv_file:
        fieldnames = ['Date',
                       'Time',
                       'Zone',
                       'Subzone',
                       'Surface temperature',
                       ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        while True:
            date, time = get_datetime()

            try:
                # Read data from IR_1
                command_1 = "1M!\r"
                IR_1.write(command_1)
                IR_1.flush()
                sleep(1)
                # read bit
                data_str_1 ="1D0!\r"
                IR_1.write(data_str_1)
                data_1 = IR_1.readline()
                IR_1.flush()
                sleep(1)
                if len(data_1.split('+'))> 1:
                    writer.writerow({'Date': date, 'Time': time, 'Zone': "B", 'Subzone': "1", 'Surface temperature': data_1})
            except Exception as e:
                now = get_datetime()
                print(f"Error reading IR_1 at {now[1]} on {now[0]}: {e}")

            try:
                # Read data from IR_2
                command_2 = "2M!\r"
                IR_2.write(command_2)
                IR_2.flush()
                sleep(2)
                # read bit
                data_str_2 ="2D0!\r"
                IR_2.write(data_str_2)
                data_2 = IR_2.readline()
                IR_2.flush()
                sleep(2)
                if len(data_2.split('+'))> 1:
                    writer.writerow({'Date': date, 'Time': time, 'Zone': "B", 'Subzone': "2", 'Surface temperature': data_2})
            except Exception as e:
                now = get_datetime()
                print(f"Error reading IR_2 at {now[0]} on {now[1]}: {e}")

            try:
                # Read data from IR_3
                command_3 = "3M!\r"
                IR_3.write(command_3)
                IR_3.flush()
                sleep(3)
                # read bit
                data_str_3 ="3D0!\r"
                IR_3.write(data_str_3)
                data_3 = IR_3.readline()
                IR_3.flush()
                sleep(3)
                if len(data_3.split('+'))> 1:
                    writer.writerow({'Date': date, 'Time': time, 'Zone': "C", 'Subzone': "1", 'Surface temperature': data_3})
            except Exception as e:
                now = get_datetime()
                print(f"Error reading IR_3 at {now[0]} on {now[1]}: {e}")

            try:
                # Read data from IR_4
                command_4 = "4M!\r"
                IR_4.write(command_4)
                IR_4.flush()
                sleep(4)
                # read bit
                data_str_4 ="4D0!\r"
                IR_4.write(data_str_4)
                data_4 = IR_4.readline()
                IR_4.flush()
                sleep(4)
                if len(data_4.split('+'))> 1:
                    writer.writerow({'Date': date, 'Time': time, 'Zone': "C", 'Subzone': "2", 'Surface temperature': data_4})
            except Exception as e:
                now = get_datetime()
                print(f"Error reading IR_4 at {now[0]} on {now[1]}: {e}")

except KeyboardInterrupt:
    # Piece of mind close out
    print("Ports Closed")
