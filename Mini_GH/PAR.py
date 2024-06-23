import minimalmodbus 
from time import sleep
import datetime
import csv
import serial
import io
import os
import logging

# Configuration of SQ-618 ID=1
PAR_1 = minimalmodbus.Instrument('/dev/ttyACM_modbus', 1)
PAR_1.serial.baudrate = 19200
PAR_1.serial.bytesize = 8
PAR_1.serial.parity = minimalmodbus.serial.PARITY_EVEN
PAR_1.serial.stopbits = 1
PAR_1.serial.timeout = 0.5
PAR_1.mode = minimalmodbus.MODE_RTU
PAR_1.clear_buffers_before_each_transaction = True
PAR_1.close_port_after_each_call = True

# Configuration of SQ-618 ID=2
PAR_2 = minimalmodbus.Instrument('/dev/ttyACM_modbus', 2)
PAR_2.serial.baudrate = 19200
PAR_2.serial.bytesize = 8
PAR_2.serial.parity = minimalmodbus.serial.PARITY_EVEN
PAR_2.serial.stopbits = 1
PAR_2.serial.timeout = 0.5
PAR_2.mode = minimalmodbus.MODE_RTU
PAR_2.clear_buffers_before_each_transaction = True
PAR_2.close_port_after_each_call = True

# Configure logging
logging.basicConfig(filename='/home/cdacea/north_GH/PAR_data.log',
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Log script start
logging.info("Script started")

# Define a function to get the current date and time in the required format
def get_datetime():
    return datetime.datetime.now()

# Define the file path for the CSV file
Climatic_data_pathway = '/home/cdacea/north_GH/PAR.csv'

# Check if the file is empty
file_exists = os.path.exists(Climatic_data_pathway) and os.path.getsize(Climatic_data_pathway) > 0

try:
    with open(Climatic_data_pathway, mode='a', newline='') as csv_file:
        fieldnames = ['datetime', 'PAR_1 (umol.m-1.s-1)', 'PAR_2 (umol.m-1.s-1)']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        # Write the header only if the file is empty
        if not file_exists:
            writer.writeheader()

        while True:
            current_datetime = get_datetime()

            # Format date and time without decimal seconds
            formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")

            try:
                PAR_intensity_1 = round(PAR_1.read_float(0, 3, 2, 0), 1)
                sleep(1)
            except Exception as e:
                logging.error(f"Error reading PAR_1: {e}")
                PAR_intensity_1 = "error"

            try:
                PAR_intensity_2 = round(PAR_2.read_float(0, 3, 2, 0), 1)
                sleep(1)
            except Exception as e:
                logging.error(f"Error reading PAR_2: {e}")
                PAR_intensity_2 = "error"

            writer.writerow({'datetime': formatted_datetime, 'PAR_1 (umol.m-1.s-1)': PAR_intensity_1, 'PAR_2 (umol.m-1.s-1)': PAR_intensity_2})

            csv_file.flush()
            os.fsync(csv_file.fileno())

            sleep(53)

except Exception as e:
    logging.error(f"Exception occurred: {e}")
finally:
    if PAR_1.serial.is_open:
        PAR_1.serial.close()
    if PAR_2.serial.is_open:
        PAR_2.serial.close()
    logging.info("Ports closed")

# Log script end
logging.info("Script ended")
