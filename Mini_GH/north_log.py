import minimalmodbus 
from time import sleep
import datetime
import csv
import serial
import io
import os
import logging

# Configure logging
logging.basicConfig(filename='/home/cdacea/north_GH/sensor_data.log',
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Configuration of SQ-618 ID=6
PAR_6 = minimalmodbus.Instrument('/dev/ttyACM_modbus', 6)
PAR_6.serial.baudrate = 19200
PAR_6.serial.bytesize = 8
PAR_6.serial.parity = minimalmodbus.serial.PARITY_EVEN
PAR_6.serial.stopbits = 1
PAR_6.serial.timeout = 0.5
PAR_6.mode = minimalmodbus.MODE_RTU
PAR_6.clear_buffers_before_each_transaction = True
PAR_6.close_port_after_each_call = True

# Configuration of SP-522 ID=10
Solar_10 = minimalmodbus.Instrument('/dev/ttyACM_modbus', 10)
Solar_10.serial.baudrate = 19200
Solar_10.serial.bytesize = 8
Solar_10.serial.parity = minimalmodbus.serial.PARITY_EVEN
Solar_10.serial.stopbits = 1
Solar_10.serial.timeout = 0.5
Solar_10.mode = minimalmodbus.MODE_RTU
Solar_10.clear_buffers_before_each_transaction = True
Solar_10.close_port_after_each_call = True

# Configuration of GMP-252 ID=41
carbo_41 = minimalmodbus.Instrument('/dev/ttyACM_modbus', 41)
carbo_41.serial.baudrate = 19200
carbo_41.serial.bytesize = 8
carbo_41.serial.parity = minimalmodbus.serial.PARITY_NONE
carbo_41.serial.stopbits = 2
carbo_41.mode = minimalmodbus.MODE_RTU
carbo_41.clear_buffers_before_each_transaction = True
carbo_41.close_port_after_each_call = True

# Configuration of HMP-155
serial_THUM = serial.Serial("/dev/ttyACM_serial",
                            baudrate=4800,
                            bytesize=serial.SEVENBITS,
                            parity=serial.PARITY_EVEN,
                            stopbits=serial.STOPBITS_ONE,
                            xonxoff=False,
                            timeout=2)
THUM_31 = io.TextIOWrapper(io.BufferedRWPair(serial_THUM, serial_THUM))

# Define a function to get the current date and time in the required format
def get_datetime():
    timenow = datetime.datetime.now()
    return timenow

# Define the file path for the CSV file
Climatic_data_pathway = '/home/cdacea/north_GH/north_climate.csv'

# Check if the file is empty
file_exists = os.path.exists(Climatic_data_pathway) and os.path.getsize(Climatic_data_pathway) > 0

try:
    with open(Climatic_data_pathway, mode='a', newline='') as csv_file:
        fieldnames = ['datetime', 'PAR_north (umol.m-1.s-1)', 'Solar radiation_north (w.m-2)', 'Temperature_north (c)', 'Humidity_north (%)', 'CO2 conc_north (ppm)']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        # Write the header only if the file is empty
        if not file_exists:
            writer.writeheader()

        while True:
            current_datetime = get_datetime()

            # Format date and time without decimal seconds
            formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")

            try:
                PAR_intensity_1 = round(PAR_6.read_float(0, 3, 2, 0), 1)
                sleep(1)
            except Exception as e:
                logging.error(f"Error reading PAR_6: {e}")
                PAR_intensity_1 = "error"

            try:
                Solar_Radiation_13 = round(Solar_10.read_float(0, 3, 2, 0), 1)
                sleep(1)
            except Exception as e:
                logging.error(f"Error reading Solar_10: {e}")
                Solar_Radiation_13 = "error"

            try:
                carbon_conc_41 = round(carbo_41.read_float(1, 3, 2, 0), 1)
                sleep(1)
            except Exception as e:
                logging.error(f"Error reading carbo_41: {e}")
                carbon_conc_41 = "error"

            try:
                THUM_31.write("OPEN 31\r\n")
                THUM_31.flush()
                sleep(1)
                THUM_31.write("SEND\r\n")
                THUM_31.flush()
                sleep(1)
                data_31 = THUM_31.readlines()
                last_line_31 = data_31[-1]
                rh_index_31 = last_line_31.find('RH=')
                temp_index_31 = last_line_31.find("Ta=")
                if rh_index_31 != -1 and temp_index_31 != -1:
                    rh_value_31 = float(last_line_31[rh_index_31 + 3:last_line_31.find('%RH')])
                    temp_value_31 = float(last_line_31[temp_index_31 + 3:last_line_31.find("'C")])
                else:
                    rh_value_31 = "error"
                    temp_value_31 = "error"
            except Exception as e:
                logging.error(f"Error reading THUM_31: {e}")
                rh_value_31 = "error"
                temp_value_31 = "error"

            writer.writerow({'datetime': formatted_datetime, 'PAR_north (umol.m-1.s-1)': PAR_intensity_1, 'Solar radiation_north (w.m-2)': Solar_Radiation_13, 'Temperature_north (c)': temp_value_31, 'Humidity_north (%)': rh_value_31, 'CO2 conc_north (ppm)': carbon_conc_41})

            csv_file.flush()
            os.fsync(csv_file.fileno())

            sleep(53)

except KeyboardInterrupt:
    if PAR_6.serial.is_open:
        PAR_6.serial.close()
    if Solar_10.serial.is_open:
        Solar_10.serial.close()
    if carbo_41.serial.is_open:
        carbo_41.serial.close()

    logging.info("Ports Closed")




