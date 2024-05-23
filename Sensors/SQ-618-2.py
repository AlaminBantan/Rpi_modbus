import minimalmodbus # Don't forget to import the library!!
from time import sleep



# Make an "instrument" object called PAR_2 (port name, slave address (in decimal))
PAR_2 = minimalmodbus.Instrument('/dev/ttyACM0',2)	

PAR_2.serial.baudrate = 19200 				# BaudRate
PAR_2.serial.bytesize = 8					# Number of data bits to be requested
PAR_2.serial.parity = minimalmodbus.serial.PARITY_EVEN	# Parity Setting here is NONE but can be ODD or EVEN
PAR_2.serial.stopbits = 1					# Number of stop bits
PAR_2.serial.timeout  = 0.5					# Timeout time in seconds
PAR_2.mode = minimalmodbus.MODE_RTU				# Mode to be used (RTU or ascii mode)

# Good practice to clean up before and after each execution
PAR_2.clear_buffers_before_each_transaction = True
PAR_2.close_port_after_each_call = True


try:
	while True:
		
		# ~ read_float(registeraddress: int, functioncode: int = 3, number_of_registers: int = 2, byteorder: int = 0) 
		PAR_intensity_2 = PAR_2.read_float(0, 3, 2, 0)
		slave_2 = PAR_2.read_float(16,3,2,0)
		Baud_2 = PAR_2.read_float(22,3,2,0)
		Parity_2 = PAR_2.read_float(24,3,2,0)
		Stopbit_2 = PAR_2.read_float(26,3,2,0)
	
		
		print("\n"*50)
		print("Sensor Data--------------------------------")
		print(f"PAR intensity is: {PAR_intensity_2} umol.m^-2")
		print(f"slaveid={slave_2}, Baud={Baud_2}, Parit={Parity_2}, Stopbit={Stopbit_2}")

		print("------------------------------------------")
		
		print("")
		print("")
		print("")
		sleep(1)
	
except KeyboardInterrupt:
	
	# Piece of mind close out
	PAR_2.serial.close()
	print("Ports Now Closed")
