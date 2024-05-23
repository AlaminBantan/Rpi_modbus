import minimalmodbus 
from time import sleep
import datetime
import csv
import time



#configuration of SQ-618 ID=1
PAR_1 = minimalmodbus.Instrument('/dev/ttyUSB0',1)	# Make an "instrument" object called PAR_1 (port name, slave address (in decimal))
PAR_1.serial.baudrate = 19200 	
PAR_1.serial.bytesize = 8					# Number of data bits to be requested
PAR_1.serial.parity = minimalmodbus.serial.PARITY_EVEN	# Parity Setting here is NONE but can be ODD or EVEN
PAR_1.serial.stopbits = 1					# Number of stop bits
PAR_1.serial.timeout  = 0.5					# Timeout time in seconds
PAR_1.mode = minimalmodbus.MODE_RTU				# Mode to be used (RTU or ascii mode)
PAR_1.clear_buffers_before_each_transaction = True
PAR_1.close_port_after_each_call = True

#configuration of SQ-618 ID=2
PAR_2 = minimalmodbus.Instrument('/dev/ttyUSB0',2)	
PAR_2.serial.baudrate = 19200 				# BaudRate
PAR_2.serial.bytesize = 8					# Number of data bits to be requested
PAR_2.serial.parity = minimalmodbus.serial.PARITY_EVEN	# Parity Setting here is NONE but can be ODD or EVEN
PAR_2.serial.stopbits = 1					# Number of stop bits
PAR_2.serial.timeout  = 0.5					# Timeout time in seconds
PAR_2.mode = minimalmodbus.MODE_RTU				# Mode to be used (RTU or ascii mode)
PAR_2.clear_buffers_before_each_transaction = True
PAR_2.close_port_after_each_call = True


#configuration of SQ-618 ID=3
PAR_3 = minimalmodbus.Instrument('/dev/ttyUSB0',3)	# Make an "instrument" object called PAR_3 (port name, slave address (in decimal))
PAR_3.serial.baudrate = 19200 	
PAR_3.serial.bytesize = 8					# Number of data bits to be requested
PAR_3.serial.parity = minimalmodbus.serial.PARITY_EVEN	# Parity Setting here is NONE but can be ODD or EVEN
PAR_3.serial.stopbits = 1					# Number of stop bits
PAR_3.serial.timeout  = 0.5					# Timeout time in seconds
PAR_3.mode = minimalmodbus.MODE_RTU	
PAR_3.clear_buffers_before_each_transaction = True
PAR_3.close_port_after_each_call = True


#configuration of SQ-618 ID=4
PAR_4 = minimalmodbus.Instrument('/dev/ttyUSB0',4)	# Make an "instrument" object called PAR_4 (port name, slave address (in decimal))
PAR_4.serial.baudrate = 19200 	
PAR_4.serial.bytesize = 8					# Number of data bits to be requested
PAR_4.serial.parity = minimalmodbus.serial.PARITY_EVEN	# Parity Setting here is NONE but can be ODD or EVEN
PAR_4.serial.stopbits = 1					# Number of stop bits
PAR_4.serial.timeout  = 0.5					# Timeout time in seconds
PAR_4.mode = minimalmodbus.MODE_RTU				# Mode to be used (RTU or ascii mode)
PAR_4.clear_buffers_before_each_transaction = True
PAR_4.close_port_after_each_call = True




# Define a function to get the current date and time in the required format
def get_datetime():
    now = datetime.datetime.now()
    return now.strftime("%m/%d/%Y"), now.strftime("%H:%M")

# Define the file path for the CSV file
PAR_carbon_csv_file_path = "/home/cdacea/GH_data/PAR.csv"

try:
    with open(PAR_carbon_csv_file_path, mode='a', newline='') as csv_file:
        fieldnames = ['Date',
                       'Time',
                       'Zone',
                       'Subzone',
                       'PAR']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        while True:
            date, time = get_datetime()

            try:
                # Read data from PAR_1
                PAR_intensity_1 = PAR_1.read_float(0, 3, 2, 0)
                sleep(4)
                writer.writerow({'Date': date, 'Time': time, 'Zone': "B", 'Subzone': "1", 'PAR': PAR_intensity_1})

            except Exception as e:
                now = get_datetime()
                print(f"Error reading PAR_1 at {now[1]} on {now[0]}: {e}")

            try:
                # Read data from PAR_2
                PAR_intensity_2 = PAR_2.read_float(0, 3, 2, 0)
                sleep(4)
                writer.writerow({'Date': date, 'Time': time, 'Zone': "B", 'Subzone': "2", 'PAR': PAR_intensity_2})
            except Exception as e:
                now = get_datetime()
                print(f"Error reading PAR_2 at {now[1]} on {now[0]}: {e}")

            try:
                # Read data from PAR_3
                PAR_intensity_3 = PAR_3.read_float(0, 3, 2, 0)
                sleep(4)
                writer.writerow({'Date': date, 'Time': time, 'Zone': "B", 'Subzone': "3", 'PAR': PAR_intensity_3})
            except Exception as e:
                now = get_datetime()
                print(f"Error reading PAR_3 at {now[1]} on {now[0]}: {e}")
            

            try:
                # Read data from PAR_4
                PAR_intensity_4 = PAR_4.read_float(0, 3, 2, 0)
                sleep(4)
                writer.writerow({'Date': date, 'Time': time, 'Zone': "C", 'Subzone': "1", 'PAR': PAR_intensity_4})
            except Exception as e:
                now = get_datetime()
                print(f"Error reading PAR_4 at {now[1]} on {now[0]}: {e}")


except KeyboardInterrupt:
    # Piece of mind close out
    PAR_1.serial.close()
    PAR_2.serial.close()
    PAR_3.serial.close()
    PAR_4.serial.close()



    print("Ports Closed")
