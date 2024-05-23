import minimalmodbus # Don't forget to import the library!!
from time import sleep



# Make an "instrument" object called carbo_43 (port name, slave address (in decimal))
carbo_43 = minimalmodbus.Instrument('/dev/ttyACM0', 43, debug=False)	

carbo_43.serial.baudrate = 19200 				# BaudRate
carbo_43.serial.bytesize = 8					# Number of data bits to be requested
carbo_43.serial.parity = minimalmodbus.serial.PARITY_NONE	# Parity Setting here is NONE but can be ODD or EVEN
carbo_43.serial.stopbits = 2					# Number of stop bits
carbo_43.mode = minimalmodbus.MODE_RTU				# Mode to be used (RTU or ascii mode)

# Good practice to clean up before and after each execution
carbo_43.clear_buffers_before_each_transaction = True
carbo_43.close_port_after_each_call = True


try:
	while True:
		
		# ~ read_float(registeraddress: int, functioncode: int = 3, number_of_registers: int = 2, byteorder: int = 0) 
		carbon_conc = carbo_43.read_float(1, 3, 2, 0)
			
		
		print("\n"*50)
		print("Sensor Data--------------------------------")
		print(f"CO2 concentration is: {carbon_conc} ppm")
		print("------------------------------------------")
		sleep(10)
	
except KeyboardInterrupt:
	
	# Piece of mind close out
	carbo_43.serial.close()
	print("Ports Now Closed")
