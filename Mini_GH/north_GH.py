import minimalmodbus 
from time import sleep
import datetime
import csv
import serial
import io
import os

# Configuration of SQ-618 ID=1
PAR_1 = minimalmodbus.Instrument('/dev/ttyACM0', 1)
PAR_1.serial.baudrate = 19200
PAR_1.serial.bytesize = 8
PAR_1.serial.parity = minimalmodbus.serial.PARITY_EVEN
PAR_1.serial.stopbits = 1
PAR_1.serial.timeout = 0.5
PAR_1.mode = minimalmodbus.MODE_RTU
PAR_1.clear_buffers_before_each_transaction = True
PAR_1.close_port_after_each_call = True

# Configuration of SP-522 ID=10
Solar_11 = minimalmodbus.Instrument('/dev/ttyACM0', 11)
Solar_11.serial.baudrate = 19200
Solar_11.serial.bytesize = 8
Solar_11.serial.parity = minimalmodbus.serial.PARITY_EVEN
Solar_11.serial.stopbits = 1
Solar_11.serial.timeout = 0.5
Solar_11.mode = minimalmodbus.MODE_RTU
Solar_11.clear_buffers_before_each_transaction = True
Solar_11.close_port_after_each_call = True


# Configuration of GMP-252 ID=41
carbo_41 = minimalmodbus.Instrument('/dev/ttyACM0',41)
carbo_41.serial.baudrate = 19200
carbo_41.serial.bytesize = 8
carbo_41.serial.parity = minimalmodbus.serial.PARITY_NONE
carbo_41.serial.stopbits = 2
carbo_41.mode = minimalmodbus.MODE_RTU
carbo_41.clear_buffers_before_each_transaction = True
carbo_41.close_port_after_each_call = True

# Configuration of HMP-155
serial_THUM = serial.Serial("/dev/ttyACM1",
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
try:
    while True:
        current_datetime = get_datetime()

        # Format date and time without decimal seconds
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

        try:
            # Read data from PAR_1 and round to 1 decimal place
            PAR_intensity_1 = round(PAR_1.read_float(0, 3, 2, 0), 1)
        except Exception as e:
            PAR_intensity_1 = "Error"

        try:
            # Read data from Solar_11 and round to 1 decimal place
            Solar_Radiation_11 = round(Solar_11.read_float(0, 3, 2, 0), 1)
        except Exception as e:
            Solar_Radiation_11 = "Error"

        try:
            # Read data from carbo_41 and round to 1 decimal place
            carbon_conc_41 = round(carbo_41.read_float(1, 3, 2, 0), 1)
        except Exception as e:
            carbon_conc_41 = "Error"

        # Read data from Thum_31
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
        except Exception as e:
            rh_value_31 = "Error"
            temp_value_31 = "Error"

        # Print the sensor readings
        print("\n"*10)
        print("--------------------------------")
        print("Climatic condition in North GH!")
        print(f"Time is {formatted_datetime}")
        print(f"PAR is {PAR_intensity_1} umol.m-2.s-1")
        print(f"Solar radiation is {Solar_Radiation_11} W.m-2")
        print(f"Temperature is {temp_value_31} C")
        print(f"Relative humidity is {rh_value_31}%")
        print(f"Carbon concentration is {carbon_conc_41} ppm")
        print("--------------------------------")

        sleep(10)

except KeyboardInterrupt:
    # Close serial ports only if they are open
    if PAR_1.serial.is_open:
        PAR_1.serial.close()
    if Solar_11.serial.is_open:
        Solar_11.serial.close()
    if carbo_41.serial.is_open:
        carbo_41.serial.close()

    print("Ports Closed")
