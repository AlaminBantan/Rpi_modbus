import minimalmodbus # Don't forget to import the library!!
from time import sleep

LW_1 = minimalmodbus.Instrument('/dev/ttyUSB0',1)	# Make an "instrument" object called LW_1 (port name, slave address (in decimal))

LW_1.serial.baudrate = 9600	
LW_1.serial.bytesize = 8					# Number of data bits to be requested
LW_1.serial.parity = minimalmodbus.serial.PARITY_NONE	# Parity Setting here is NONE but can be ODD or EVEN
LW_1.serial.stopbits = 1					# Number of stop bits
LW_1.serial.timeout  = 0.5					# Timeout time in seconds
LW_1.mode = minimalmodbus.MODE_RTU				# Mode to be used (RTU or ascii mode)

# Good practice to clean up before and after each execution
LW_1.clear_buffers_before_each_transaction = True
LW_1.close_port_after_each_call = True


try:
	while True:
		
		# ~ read_float(registeraddress: int, functioncode: int = 3, number_of_registers: int = 2, byteorder: int = 0) 
		LW_intensity_1 = LW_1.read_float(1, 3, 2, 0)

	
		
		print("\n"*50)
		print("Sensor Data--------------------------------")
		print(f"LW is: {LW_intensity_1}")


		print("------------------------------------------")
		
		print("")
		print("")
		print("")
		sleep(1)
	
	
except KeyboardInterrupt:
	
	# Piece of mind close out
	LW_1.serial.close()
	print("Ports Now Closed")
