import minimalmodbus
from time import sleep
import datetime
import csv
import serial
import io
import os
import logging

# Configure logging
logging.basicConfig(filename='/home/cdacea/south_GH/sensor_data.log',
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Configuration of SQ-618 ID=5
PAR_2 = minimalmodbus.Instrument('/dev/ttyACM_modbus', 2)
PAR_2.serial.baudrate = 19200
PAR_2.serial.bytesize = 8
PAR_2.serial.parity = minimalmodbus.serial.PARITY_EVEN
PAR_2.serial.stopbits = 1
PAR_2.serial.timeout = 0.5
PAR_2.mode = minimalmodbus.MODE_RTU
PAR_2.clear_buffers_before_each_transaction = True
PAR_2.close_port_after_each_call = True

# Configuration of SP-522 ID=10
Solar_12 = minimalmodbus.Instrument('/dev/ttyACM_modbus', 12)
Solar_12.serial.baudrate = 19200
Solar_12.serial.bytesize = 8
Solar_12.serial.parity = minimalmodbus.serial.PARITY_EVEN
Solar_12.serial.stopbits = 1
Solar_12.serial.timeout = 0.5
Solar_12.mode = minimalmodbus.MODE_RTU
Solar_12.clear_buffers_before_each_transaction = True
Solar_12.close_port_after_each_call = True

# Configuration of GMP-252 ID=41
carbo_42 = minimalmodbus.Instrument('/dev/ttyACM_modbus', 42)
carbo_42.serial.baudrate = 19200
carbo_42.serial.bytesize = 8
carbo_42.serial.parity = minimalmodbus.serial.PARITY_NONE
carbo_42.serial.stopbits = 2
carbo_42.mode = minimalmodbus.MODE_RTU
carbo_42.clear_buffers_before_each_transaction = True
carbo_42.close_port_after_each_call = True

# Configuration of HMP-155
serial_THUM = serial.Serial("/dev/ttyACM_serial",
                            baudrate=4800,
                            bytesize=serial.SEVENBITS,
                            parity=serial.PARITY_EVEN,
                            stopbits=serial.STOPBITS_ONE,
                            xonxoff=False,
                            timeout=2)
THUM_32 = io.TextIOWrapper(io.BufferedRWPair(serial_THUM, serial_THUM))

# Define a function to get the current date and time in the required format
def get_datetime():
    return datetime.datetime.now()

# Define the file path for the CSV file
Climatic_data_pathway = '/home/cdacea/south_GH/south_climate.csv'

# Check if the file is empty
file_exists = os.path.exists(Climatic_data_pathway) and os.path.getsize(Climatic_data_pathway) > 0

try:
    with open(Climatic_data_pathway, mode='a', newline='') as csv_file:
        fieldnames = ['datetime', 'PAR_south (umol.m-1.s-1)', 'Solar radiation_south (w.m-2)', 'Temperature_south (c)', 'Humidity_south (%)', 'CO2 conc_south (ppm)']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        # Write the header only if the file is empty
        if not file_exists:
            writer.writeheader()

        while True:
            current_datetime = get_datetime()

            # Format date and time without decimal seconds
            formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")

            try:
                PAR_intensity_2 = round(PAR_2.read_float(0, 3, 2, 0), 1)
                sleep(1)
            except Exception as e:
                logging.error(f"Error reading PAR_2: {e}")
                PAR_intensity_2 = "error"

            try:
                Solar_Radiation_12 = round(Solar_12.read_float(0, 3, 2, 0), 1)
                sleep(1)
            except Exception as e:
                logging.error(f"Error reading Solar_12: {e}")
                Solar_Radiation_12 = "error"

            try:
                carbon_conc_42 = round(carbo_42.read_float(1, 3, 2, 0), 1)
                sleep(1)
            except Exception as e:
                logging.error(f"Error reading carbo_42: {e}")
                carbon_conc_42 = "error"

            try:
                THUM_32.write("OPEN 32\r\n")
                THUM_32.flush()
                sleep(1)
                THUM_32.write("SEND\r\n")
                THUM_32.flush()
                sleep(1)
                data_32 = THUM_32.readlines()
                last_line_32 = data_32[-1]
                rh_index_32 = last_line_32.find('RH=')
                temp_index_32 = last_line_32.find("Ta=")
                if rh_index_32 != -1 and temp_index_32 != -1:
                    rh_value_32 = float(last_line_32[rh_index_32 + 3:last_line_32.find('%RH')])
                    temp_value_32 = float(last_line_32[temp_index_32 + 3:last_line_32.find("'C")])
                else:
                    rh_value_32 = "error"
                    temp_value_32 = "error"
            except Exception as e:
                logging.error(f"Error reading THUM_32: {e}")
                rh_value_32 = "error"
                temp_value_32 = "error"

            writer.writerow({'datetime': formatted_datetime, 'PAR_south (umol.m-1.s-1)': PAR_intensity_2, 'Solar radiation_south (w.m-2)': Solar_Radiation_12, 'Temperature_south (c)': temp_value_32, 'Humidity_south (%)': rh_value_32, 'CO2 conc_south (ppm)': carbon_conc_42})

            csv_file.flush()
            os.fsync(csv_file.fileno())

            sleep(53)

except KeyboardInterrupt:
    if PAR_2.serial.is_open:
        PAR_2.serial.close()
    if Solar_12.serial.is_open:
        Solar_12.serial.close()
    if carbo_42.serial.is_open:
        carbo_42.serial.close()
    logging.info("Ports Closed")
