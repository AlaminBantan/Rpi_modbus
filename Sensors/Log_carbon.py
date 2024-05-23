import minimalmodbus 
from time import sleep
import datetime
import csv
import time


#configuration of GMP-252 ID=41
carbo_41 = minimalmodbus.Instrument('/dev/ttyUSB0', 41)	
carbo_41.serial.baudrate = 19200 				# BaudRate
carbo_41.serial.bytesize = 8					# Number of data bits to be requested
carbo_41.serial.parity = minimalmodbus.serial.PARITY_NONE	# Parity Setting here is NONE but can be ODD or EVEN
carbo_41.serial.stopbits = 2					# Number of stop bits
carbo_41.mode = minimalmodbus.MODE_RTU				# Mode to be used (RTU or ascii mode)
carbo_41.clear_buffers_before_each_transaction = True
carbo_41.close_port_after_each_call = True

#configuration of GMP-252 ID=42
carbo_42 = minimalmodbus.Instrument('/dev/ttyUSB0', 42)	
carbo_42.serial.baudrate = 19200 				# BaudRate
carbo_42.serial.bytesize = 8					# Number of data bits to be requested
carbo_42.serial.parity = minimalmodbus.serial.PARITY_NONE	# Parity Setting here is NONE but can be ODD or EVEN
carbo_42.serial.stopbits = 2					# Number of stop bits
carbo_42.mode = minimalmodbus.MODE_RTU				# Mode to be used (RTU or ascii mode)
carbo_42.clear_buffers_before_each_transaction = True
carbo_42.close_port_after_each_call = True


# Define a function to get the current date and time in the required format
def get_datetime():
    now = datetime.datetime.now()
    return now.strftime("%m/%d/%Y"), now.strftime("%H:%M")

# Define the file path for the CSV file
Carbon_csv_file_path = "/home/cdacea/GH_data/Carbon.csv"

try:
    with open(Carbon_csv_file_path, mode='a', newline='') as csv_file:
        fieldnames = ['Date',
                       'Time',
                       'Zone',
                       'Subzone',
                       'CO2 ppm']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        while True:
            date, time = get_datetime()
            try:
                carbon_conc_41 = carbo_41.read_float(1, 3, 2, 0)
                sleep(4)
                writer.writerow({'Date': date, 'Time': time, 'Zone': "B", 'Subzone': "1", 'CO2 ppm': carbon_conc_41})
            except Exception as e:
                now = get_datetime()
                print(f"Error reading carbo_41 at {now[1]} on {now[0]}: {e}")
            try:
                carbon_conc_42 = carbo_42.read_float(1, 3, 2, 0)
                sleep(4)
                writer.writerow({'Date': date, 'Time': time, 'Zone': "B", 'Subzone': "1", 'CO2 ppm': carbon_conc_42})
            except Exception as e:
                now = get_datetime()
                print(f"Error reading carbo_42 at {now[1]} on {now[0]}: {e}")
    





except KeyboardInterrupt:
    # Piece of mind close out
    carbo_41.serial.close()
    carbo_42.serial.close()


    print("Ports Closed")
