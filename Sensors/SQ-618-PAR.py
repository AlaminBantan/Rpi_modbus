import minimalmodbus
from time import sleep, strftime
import csv
import os

PAR_1 = minimalmodbus.Instrument('/dev/ttyUSB0',1)	# Make an "instrument" object called PAR_1 (port name, slave address (in decimal))

PAR_1.serial.baudrate = 19200 	
PAR_1.serial.bytesize = 8					# Number of data bits to be requested
PAR_1.serial.parity = minimalmodbus.serial.PARITY_EVEN	# Parity Setting here is NONE but can be ODD or EVEN
PAR_1.serial.stopbits = 1					# Number of stop bits
PAR_1.serial.timeout  = 0.5					# Timeout time in seconds
PAR_1.mode = minimalmodbus.MODE_RTU				# Mode to be used (RTU or ascii mode)

# Good practice to clean up before and after each execution
PAR_1.clear_buffers_before_each_transaction = True
PAR_1.close_port_after_each_call = True

csv_header = ["Date", "Time", "PAR Intensity in zone b (umol.m^-2.s^-1)"]

while True:
    # Get current date and time
    current_date = strftime("%m-%d-%Y")
    current_time = strftime("%H:%M")

    # Check if it's a new day and create a new CSV file
    if not os.path.exists(f"data_{current_date}.csv"):
        with open(f"data_{current_date}.csv", mode="w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(csv_header)

    # Read light intensity from the sensor
    PAR_intensity = PAR_1.read_float(0, 3, 2, 0)

    # Append data to the current day's CSV file
    with open(f"data_{current_date}.csv", mode="a", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([current_date, current_time, PAR_intensity])

    # Check if it's past 12 AM, and if so, exit the loop
    if current_time >= "23:59:59":
        break

    sleep(60)

PAR_1.serial.close()
print("Ports Now Closed")
