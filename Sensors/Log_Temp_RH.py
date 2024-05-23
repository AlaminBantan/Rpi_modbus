import serial
import io
import csv
import re
from time import sleep
from datetime import datetime

serial_THUM = serial.Serial("/dev/ttyACM0",
                   baudrate=4800,
                   bytesize=serial.SEVENBITS,
                   parity=serial.PARITY_EVEN,
                   stopbits=serial.STOPBITS_ONE,
                   xonxoff=False,
                   timeout=2)

THUM_31 = io.TextIOWrapper(io.BufferedRWPair(serial_THUM, serial_THUM))
THUM_32 = io.TextIOWrapper(io.BufferedRWPair(serial_THUM, serial_THUM))
THUM_33 = io.TextIOWrapper(io.BufferedRWPair(serial_THUM, serial_THUM))
THUM_34 = io.TextIOWrapper(io.BufferedRWPair(serial_THUM, serial_THUM))


# Define a function to get the current date and time in the required format
def get_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y"), now.strftime("%H:%M")

# Define the file path for the CSV file
Temp_RH_csv_file_path = "/home/cdacea/GH_data/Temp_RH.csv"

try:
    with open(Temp_RH_csv_file_path, mode='a', newline='') as csv_file:
        fieldnames = ['Date', 'Time', 'Zone', 'Subzone', 'Ambient temperature', 'Relative humidity']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        while True:
            date, time = get_datetime()

            try:
                # Read data from THUM_31
                THUM_31.write("OPEN 31\r\n")
                THUM_31.flush()
                print("31 is opened")
                sleep(3)

                THUM_31.write("SEND\r\n")
                THUM_31.flush()
                print("send")
                sleep(3)
        
                data_31 = THUM_31.readlines()
                # Extract RH and Ta from the data
                rh_match = re.search(r'RH= (\d+\.\d+)', data_31[-1])
                ta_match = re.search(r'Ta= (\d+\.\d+)', data_31[-1])

                if rh_match and ta_match:
                    rh_value = rh_match.group(1)
                    ta_value = ta_match.group(1)

                    # Get current date and time
                    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Print the data
                    writer.writerow({'Date': date, 'Time': time, 'Zone': "B", 'Subzone': "1", 'Ambient temperature': ta_value, 'Relative humidity': rh_value})
                    sleep(3)

                    THUM_31.write("CLOSE\r\n")
                    print("closed")
                    sleep(10)
            except Exception as e:
                # Handle specific exceptions if needed
                print(f"Error for THUM_31: {str(e)}")

            try:
                # Read data from THUM_32
                THUM_32.write("OPEN 32\r\n")
                THUM_32.flush()
                print("32 is opened")
                sleep(3)

                THUM_32.write("SEND\r\n")
                THUM_32.flush()
                print("send")
                sleep(3)
        
                data_32 = THUM_32.readlines()
                # Extract RH and Ta from the data
                rh_match = re.search(r'RH= (\d+\.\d+)', data_32[-1])
                ta_match = re.search(r'Ta= (\d+\.\d+)', data_32[-1])

                if rh_match and ta_match:
                    rh_value = rh_match.group(1)
                    ta_value = ta_match.group(1)

                    # Get current date and time
                    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Print the data
                    writer.writerow({'Date': date, 'Time': time, 'Zone': "B", 'Subzone': "2", 'Ambient temperature': ta_value, 'Relative humidity': rh_value})
                    sleep(3)

                    THUM_32.write("CLOSE\r\n")
                    print("closed")
                    sleep(10)
            except Exception as e:
                # Handle specific exceptions if needed
                print(f"Error for THUM_32: {str(e)}")

            try:
                # Read data from THUM_33
                THUM_33.write("OPEN 33\r\n")
                THUM_33.flush()
                print("33 is opened")
                sleep(3)

                THUM_33.write("SEND\r\n")
                THUM_33.flush()
                print("send")
                sleep(10)
            
                data_33 = THUM_33.readlines()
                # Extract RH and Ta from the data
                rh_match = re.search(r'RH= (\d+\.\d+)', data_33[-1])
                ta_match = re.search(r'Ta= (\d+\.\d+)', data_33[-1])

                if rh_match and ta_match:
                    rh_value = rh_match.group(1)
                    ta_value = ta_match.group(1)

                    # Get current date and time
                    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Print the data
                    writer.writerow({'Date': date, 'Time': time, 'Zone': "C", 'Subzone': "1", 'Ambient temperature': ta_value, 'Relative humidity': rh_value})
                    sleep(3)

                    THUM_33.write("CLOSE\r\n")
                    print("closed")
                    sleep(10)
            except Exception as e:
                # Handle specific exceptions if needed
                print(f"Error for THUM_33: {str(e)}")

            try:
                # Read data from THUM_34
                THUM_34.write("OPEN 34\r\n")
                THUM_34.flush()
                print("34 is opened")
                sleep(3)

                THUM_34.write("SEND\r\n")
                THUM_34.flush()
                print("send")
                sleep(3)
            
                data_34 = THUM_34.readlines()
                # Extract RH and Ta from the data
                rh_match = re.search(r'RH= (\d+\.\d+)', data_34[-1])
                ta_match = re.search(r'Ta= (\d+\.\d+)', data_34[-1])

                if rh_match and ta_match:
                    rh_value = rh_match.group(1)
                    ta_value = ta_match.group(1)

                    # Get current date and time
                    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Print the data
                    writer.writerow({'Date': date, 'Time': time, 'Zone': "C", 'Subzone': "2", 'Ambient temperature': ta_value, 'Relative humidity': rh_value})
                    sleep(3)

                    THUM_34.write("CLOSE\r\n")
                    print("closed")
                    sleep(10)
            except Exception as e:
                # Handle specific exceptions if needed
                print(f"Error for THUM_34: {str(e)}")

except KeyboardInterrupt:
    # Clean up when interrupted
    print("Ports Now Closed")
