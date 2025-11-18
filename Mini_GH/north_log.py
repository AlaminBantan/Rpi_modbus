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

# --- Sensor Configurations ---

# SQ-618 PAR Sensor (ID=6)
sq618_6 = minimalmodbus.Instrument('/dev/ttyACM_modbus', 6)
sq618_6.serial.baudrate = 19200
sq618_6.serial.bytesize = 8
sq618_6.serial.parity = minimalmodbus.serial.PARITY_EVEN
sq618_6.serial.stopbits = 1
sq618_6.serial.timeout = 0.8
sq618_6.mode = minimalmodbus.MODE_RTU
sq618_6.clear_buffers_before_each_transaction = True
sq618_6.close_port_after_each_call = True

# SP-522 Solar Radiation Sensor (ID=10)
sp522_10 = minimalmodbus.Instrument('/dev/ttyACM_modbus', 10)
sp522_10.serial.baudrate = 19200
sp522_10.serial.bytesize = 8
sp522_10.serial.parity = minimalmodbus.serial.PARITY_EVEN
sp522_10.serial.stopbits = 1
sp522_10.serial.timeout = 0.8
sp522_10.mode = minimalmodbus.MODE_RTU
sp522_10.clear_buffers_before_each_transaction = True
sp522_10.close_port_after_each_call = True

# GMP-252 CO₂ Sensor (ID=41)
gmp252_41 = minimalmodbus.Instrument('/dev/ttyACM_modbus', 41)
gmp252_41.serial.baudrate = 19200
gmp252_41.serial.bytesize = 8
gmp252_41.serial.parity = minimalmodbus.serial.PARITY_NONE
gmp252_41.serial.stopbits = 2
gmp252_41.serial.timeout = 0.8
gmp252_41.mode = minimalmodbus.MODE_RTU
gmp252_41.clear_buffers_before_each_transaction = True
gmp252_41.close_port_after_each_call = True

# HMP-155 Temperature & Humidity Sensor
serial_THUM = serial.Serial("/dev/ttyACM_serial",
                            baudrate=4800,
                            bytesize=serial.SEVENBITS,
                            parity=serial.PARITY_EVEN,
                            stopbits=serial.STOPBITS_ONE,
                            xonxoff=False,
                            timeout=2)
THUM_31 = io.TextIOWrapper(io.BufferedRWPair(serial_THUM, serial_THUM))

# --- Helper Functions ---
def get_datetime():
    return datetime.datetime.now()

# File Path
Climatic_data_pathway = '/home/cdacea/north_GH/north_climate.csv'
file_exists = os.path.exists(Climatic_data_pathway) and os.path.getsize(Climatic_data_pathway) > 0

# --- Main Loop ---
try:
    with open(Climatic_data_pathway, mode='a', newline='') as csv_file:
        fieldnames = ['datetime', 'PAR_north (umol.m-2.s-1)', 'Solar radiation_north (W.m-2)',
                      'Temperature_north (°C)', 'Humidity_north (%)', 'CO2 conc_north (ppm)']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        while True:
            current_datetime = get_datetime()
            formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")

            # SQ-618
            try:
                par_value = round(sq618_6.read_float(0, 3, 2, 0), 1)
                sleep(1)
            except Exception as e:
                logging.error(f"Error reading sq618_6: {e}")
                par_value = "error"

            # SP-522
            try:
                solar_value = round(sp522_10.read_float(0, 3, 2, 0), 1)
                sleep(1)
            except Exception as e:
                logging.error(f"Error reading sp522_10: {e}")
                solar_value = "error"

            # GMP-252
            try:
                co2_value = round(gmp252_41.read_float(1, 3, 2, 0), 1)
                sleep(1)
            except Exception as e:
                logging.error(f"Error reading gmp252_41: {e}")
                co2_value = "error"

            # HMP-155
            try:
                THUM_31.write("OPEN 31\r\n")
                THUM_31.flush()
                sleep(1)
                THUM_31.write("SEND\r\n")
                THUM_31.flush()
                sleep(1)
                data_31 = THUM_31.readlines()
                last_line_31 = data_31[-1]
                rh_index = last_line_31.find('RH=')
                temp_index = last_line_31.find("Ta=")
                if rh_index != -1 and temp_index != -1:
                    rh_value = float(last_line_31[rh_index + 3:last_line_31.find('%RH')])
                    temp_value = float(last_line_31[temp_index + 3:last_line_31.find("'C")])
                else:
                    rh_value = "error"
                    temp_value = "error"
            except Exception as e:
                logging.error(f"Error reading THUM_31: {e}")
                rh_value = "error"
                temp_value = "error"

            writer.writerow({'datetime': formatted_datetime,
                             'PAR_north (umol.m-2.s-1)': par_value,
                             'Solar radiation_north (W.m-2)': solar_value,
                             'Temperature_north (°C)': temp_value,
                             'Humidity_north (%)': rh_value,
                             'CO2 conc_north (ppm)': co2_value})
            csv_file.flush()
            os.fsync(csv_file.fileno())

            sleep(53)

except KeyboardInterrupt:
    if sq618_6.serial.is_open:
        sq618_6.serial.close()
    if sp522_10.serial.is_open:
        sp522_10.serial.close()
    if gmp252_41.serial.is_open:
        gmp252_41.serial.close()
    logging.info("Ports Closed")






