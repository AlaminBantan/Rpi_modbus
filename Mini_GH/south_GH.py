import minimalmodbus 
from time import sleep
import datetime
import csv
import serial
import io
import os

# Configuration of SQ-618 ID=5
PAR_2 = minimalmodbus.Instrument('/dev/ttyACM0', 2)
PAR_2.serial.baudrate = 19200
PAR_2.serial.bytesize = 8
PAR_2.serial.parity = minimalmodbus.serial.PARITY_EVEN
PAR_2.serial.stopbits = 1
PAR_2.serial.timeout = 0.5
PAR_2.mode = minimalmodbus.MODE_RTU
PAR_2.clear_buffers_before_each_transaction = True
PAR_2.close_port_after_each_call = True

# Configuration of SP-522 ID=10
Solar_12 = minimalmodbus.Instrument('/dev/ttyACM0', 12)
Solar_12.serial.baudrate = 19200
Solar_12.serial.bytesize = 8
Solar_12.serial.parity = minimalmodbus.serial.PARITY_EVEN
Solar_12.serial.stopbits = 1
Solar_12.serial.timeout = 0.5
Solar_12.mode = minimalmodbus.MODE_RTU
Solar_12.clear_buffers_before_each_transaction = True
Solar_12.close_port_after_each_call = True


# Configuration of GMP-252 ID=41
carbo_42 = minimalmodbus.Instrument('/dev/ttyACM0',42)
carbo_42.serial.baudrate = 19200
carbo_42.serial.bytesize = 8
carbo_42.serial.parity = minimalmodbus.serial.PARITY_NONE
carbo_42.serial.stopbits = 2
carbo_42.mode = minimalmodbus.MODE_RTU
carbo_42.clear_buffers_before_each_transaction = True
carbo_42.close_port_after_each_call = True

# Configuration of HMP-155
serial_THUM = serial.Serial("/dev/ttyACM1",
                   baudrate=4800,
                  bytesize=serial.SEVENBITS,
                   parity=serial.PARITY_EVEN,
                   stopbits=serial.STOPBITS_ONE,
                   xonxoff=False,
                   timeout=2)
THUM_32 = io.TextIOWrapper(io.BufferedRWPair(serial_THUM, serial_THUM))

# Define a function to get the current date and time in the required format
def get_datetime():
    timenow = datetime.datetime.now()
    return timenow
try:
    while True:
        current_datetime = get_datetime()

        # Format date and time without decimal seconds
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

        try:
            # Read data from PAR_2 and round to 1 decimal place
            PAR_intensity_2 = round(PAR_2.read_float(0, 3, 2, 0), 1)
        except Exception as e:
            PAR_intensity_2 = f"Error reading PAR_2: {e}"

        try:
            # Read data from Solar_12 and round to 1 decimal place
            Solar_Radiation_12 = round(Solar_12.read_float(0, 3, 2, 0), 1)
        except Exception as e:
            Solar_Radiation_12 = f"Error reading Solar_12: {e}"

        try:
            # Read data from carbo_42 and round to 1 decimal place
            carbon_conc_42 = round(carbo_42.read_float(1, 3, 2, 0), 1)
        except Exception as e:
            carbon_conc_42 = f"Error reading carbo_42: {e}"

        # Read data from THUM_32
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
        except Exception as e:
            rh_value_32 = f"Error reading Thum_32: {e}"
            temp_value_32 = f"Error reading Thum_32: {e}"

        # Print the sensor readings
        print("\n"*10)
        print("--------------------------------")
        print("Climatic condition in South GH!")
        print(f"Time is {formatted_datetime}")
        print(f"PAR is {PAR_intensity_2} umol.m-2.s-1")
        print(f"Solar radiation is {Solar_Radiation_12} W.m-2")
        print(f"Temperature is {temp_value_32} C")
        print(f"Relative humidity is {rh_value_32}%")
        print(f"Carbon concentration is {carbon_conc_42} ppm")
        print("--------------------------------")

        sleep(10)

except KeyboardInterrupt:
    # Close serial ports only if they are open
    if PAR_2.serial.is_open:
        PAR_2.serial.close()
    if Solar_12.serial.is_open:
        Solar_12.serial.close()
    if carbo_42.serial.is_open:
        carbo_42.serial.close()

    print("Ports Closed")
