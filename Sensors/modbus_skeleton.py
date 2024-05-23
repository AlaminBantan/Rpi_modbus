"""
######################################################################

Simple Modbus Sensor Polling Code
Coded By "The Intrigued Engineer" over a coffee

Minimal Modbus Library Documentation
https://minimalmodbus.readthedocs.io/en/stable/

Thanks For Watching!!!

######################################################################
"""

import minimalmodbus # Don't forget to import the library!!
from time import sleep


mb_address = 1 # Modbus address of sensor

sensy_boi = minimalmodbus.Instrument('/dev/ttyUSB0',mb_address)	# Make an "instrument" object called sensy_boi (port name, slave address (in decimal))

sensy_boi.serial.baudrate = 19200 				# BaudRate
sensy_boi.serial.bytesize = 8					# Number of data bits to be requested
sensy_boi.serial.parity = minimalmodbus.serial.PARITY_EVEN	# Parity Setting here is NONE but can be ODD or EVEN
sensy_boi.serial.stopbits = 1					# Number of stop bits
sensy_boi.serial.timeout  = 0.5					# Timeout time in seconds
sensy_boi.mode = minimalmodbus.MODE_RTU				# Mode to be used (RTU or ascii mode)

# Good practice to clean up before and after each execution
sensy_boi.clear_buffers_before_each_transaction = True
sensy_boi.close_port_after_each_call = True

## Uncomment this line to print out all the properties of the setup a the begining of the loop
#print(sensy_boi) 

# ~ print("")
# ~ print("Requesting Data From Sensor...")	# Makes it look cool....

# NOTE-- Register addresses are offset from 40001 so inputting register 0 in the code is actually 40001, 3 = 40004 etc...

## Example of reading SINGLE register
## Arguments - (register address, number of decimals, function code, Is the value signed or unsigned) 
## Uncomment to run this to just get temperature data

#single_data= sensy_boi.read_register(1, 1, 3, False) 
#print (f"Single register data = {single_data}")

# Get list of values from MULTIPLE registers 
# Arguments - (register start address, number of registers to read, function code) 
# ~ data =sensy_boi.read_registers(0, 2, 3) 

# ~ print("")
# ~ print(f"Raw data is {data}") # Shows the raw data list for the lolz

# Process the raw data by deviding by 10 to get the actual floating point values
# ~ hum = data[0]/10
# ~ temp = data[1]/10

# Print out the processed data in a little table
# Pro-tip > \u00B0 is the unicode value for the degree symbol which you can see before the "C" in temperature
# ~ print("-------------------------------------")
# ~ print(f"Temperature = {temp}\u00B0C")
# ~ print(f"Relative Humidity = {hum}%")
# ~ print("-------------------------------------")
# ~ print("")


try:
	while True:
		
		data =sensy_boi.read_registers(40, 7, 3) 
		
		light16 = data[0]
			
		# ~ read_float(registeraddress: int, functioncode: int = 3, number_of_registers: int = 2, byteorder: int = 0) 
		light32 = sensy_boi.read_float(0, 3, 2, 0) 
		decmv =  sensy_boi.read_float(2, 3, 2, 0) 
		imm =  sensy_boi.read_float(4, 3, 2, 0) 
		sol =  sensy_boi.read_float(6, 3, 2, 0) 
		mb_add =  int(sensy_boi.read_float(16, 3, 2, 0) )
		
		
		print("\n"*50)
		print("Sensor Data--------------------------------")
		print(f"Light Intensity 32 bit: {light32} umol.m^-2.s^-1")
		print(f"Light Intensity: 16 bit {light16/10} umol.m^-2.s^-1")
		print(f"Detector Millivolts: {decmv} V")
		print(f"Immersed Output: {imm} umol.m^-2.s^-1")
		print(f"Solar Output: {sol} umol.m^-2.s^-1")
		print(f"List of 16 bit data: {data}")
		print(f"Modbus Address: {mb_add}")
		print("------------------------------------------")
		
		
		
		print("")
		print("")
		print("")
		sleep(0.5)
	
except KeyboardInterrupt:
	
	# Piece of mind close out
	sensy_boi.serial.close()
	print("Ports Now Closed")

