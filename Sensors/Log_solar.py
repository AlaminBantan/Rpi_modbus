import minimalmodbus 
from time import sleep
import datetime
import csv
import time



#configuration of SP-522 ID=11
Solar_11 = minimalmodbus.Instrument('/dev/ttyUSB0', 11, debug=False)
Solar_11.serial.baudrate = 19200
Solar_11.serial.bytesize = 8					# Number of data bits to be requested
Solar_11.serial.parity = minimalmodbus.serial.PARITY_EVEN	# Parity Setting here is NONE but can be ODD or EVEN
Solar_11.serial.stopbits = 1					# Number of stop bits
Solar_11.serial.timeout  = 0.5					# Timeout time in seconds
Solar_11.mode = minimalmodbus.MODE_RTU			
Solar_11.clear_buffers_before_each_transaction = True
Solar_11.close_port_after_each_call = True

#configuration of SP-522 ID=12
Solar_12 = minimalmodbus.Instrument('/dev/ttyUSB0', 12, debug=False)
Solar_12.serial.baudrate = 19200
Solar_12.serial.bytesize = 8					# Number of data bits to be requested
Solar_12.serial.parity = minimalmodbus.serial.PARITY_EVEN	# Parity Setting here is NONE but can be ODD or EVEN
Solar_12.serial.stopbits = 1					# Number of stop bits
Solar_12.serial.timeout  = 0.5					# Timeout time in seconds
Solar_12.mode = minimalmodbus.MODE_RTU	
Solar_12.clear_buffers_before_each_transaction = True
Solar_12.close_port_after_each_call = True

#configuration of SP-522 ID=13
Solar_13 = minimalmodbus.Instrument('/dev/ttyUSB0', 13, debug=False)
Solar_13.serial.baudrate = 19200
Solar_13.serial.bytesize = 8					# Number of data bits to be requested
Solar_13.serial.parity = minimalmodbus.serial.PARITY_EVEN	# Parity Setting here is NONE but can be ODD or EVEN
Solar_13.serial.stopbits = 1					# Number of stop bits
Solar_13.serial.timeout  = 0.5					# Timeout time in seconds
Solar_13.mode = minimalmodbus.MODE_RTU			
Solar_13.clear_buffers_before_each_transaction = True
Solar_13.close_port_after_each_call = True

#configuration of SP-522 ID=14
Solar_14 = minimalmodbus.Instrument('/dev/ttyUSB0', 14, debug=False)
Solar_14.serial.baudrate = 19200
Solar_14.serial.bytesize = 8					# Number of data bits to be requested
Solar_14.serial.parity = minimalmodbus.serial.PARITY_EVEN	# Parity Setting here is NONE but can be ODD or EVEN
Solar_14.serial.stopbits = 1					# Number of stop bits
Solar_14.serial.timeout  = 0.5					# Timeout time in seconds
Solar_14.mode = minimalmodbus.MODE_RTU	
Solar_14.clear_buffers_before_each_transaction = True
Solar_14.close_port_after_each_call = True


# Define a function to get the current date and time in the required format
def get_datetime():
    now = datetime.datetime.now()
    return now.strftime("%m/%d/%Y"), now.strftime("%H:%M")

# Define the file path for the CSV file
Solar_csv_file_path = "/home/cdacea/GH_data/Solar.csv"

try:
    with open(Solar_csv_file_path, mode='a', newline='') as csv_file:
        fieldnames = ['Date',
                       'Time',
                       'Zone',
                       'Subzone',
                       'Solar radiation']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        while True:
            date, time = get_datetime()

            try:
                # Read data from Solar_11
                Solar_Radiation_11 = Solar_11.read_float(0, 3, 2, 0)
                sleep(4)
                writer.writerow({'Date': date, 'Time': time, 'Zone': "B", 'Subzone': "2", 'Solar radiation': Solar_Radiation_11})
            except Exception as e:
                now = get_datetime()
                print(f"Error reading Solar_11 at {now[1]} on {now[0]}: {e}")
    

            try:
                # Read data from Solar_12
                Solar_Radiation_12 = Solar_12.read_float(0, 3, 2, 0)
                sleep(4)
                writer.writerow({'Date': date, 'Time': time, 'Zone': "B", 'Subzone': "3", 'Solar radiation': Solar_Radiation_12})
            except Exception as e:
                now = get_datetime()
                print(f"Error reading Solar_12 at {now[1]} on {now[0]}: {e}")


            try:
                # Read data from Solar_13
                Solar_Radiation_13 = Solar_13.read_float(0, 3, 2, 0)
                sleep(4)
                writer.writerow({'Date': date, 'Time': time, 'Zone': "C", 'Subzone': "1", 'Solar radiation': Solar_Radiation_13})
            except Exception as e:
                now = get_datetime()
                print(f"Error reading Solar_13 at {now[1]} on {now[0]}: {e}")

                
            try:
                # Read data from Solar_14
                Solar_Radiation_14 = Solar_14.read_float(0, 3, 2, 0)
                sleep(4)
                writer.writerow({'Date': date, 'Time': time, 'Zone': "C", 'Subzone': "2", 'Solar radiation': Solar_Radiation_14})
            except Exception as e:
                now = get_datetime()
                print(f"Error reading Solar_14 at {now[1]} on {now[0]}: {e}")


except KeyboardInterrupt:
    # Piece of mind close out
    Solar_11.serial.close()
    Solar_12.serial.close()
    Solar_13.serial.close()
    Solar_14.serial.close()
    print("Ports Closed")
