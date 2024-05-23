import minimalmodbus # Don't forget to import the library!!
from time import sleep

PAR_1 = minimalmodbus.Instrument('/dev/ttyACM0',1)	# Make an "instrument" object called PAR_1 (port name, slave address (in decimal))

PAR_1.serial.baudrate = 19200 	
PAR_1.serial.bytesize = 8					# Number of data bits to be requested
PAR_1.serial.parity = minimalmodbus.serial.PARITY_NONE	# Parity Setting here is NONE but can be ODD or EVEN
PAR_1.serial.stopbits = 1					# Number of stop bits
PAR_1.serial.timeout  = 0.5					# Timeout time in seconds
PAR_1.mode = minimalmodbus.MODE_RTU				# Mode to be used (RTU or ascii mode)

# Good practice to clean up before and after each execution
PAR_1.clear_buffers_before_each_transaction = True
PAR_1.close_port_after_each_call = True


try:
	while True:
		
		# ~ read_float(registeraddress: int, functioncode: int = 3, number_of_registers: int = 2, byteorder: int = 0) 
		PAR_intensity_1 = PAR_1.read_float(0, 3, 2, 0)
		slave_1 = PAR_1.read_float(16,3,2,0)
		Baud_1 = PAR_1.read_float(22,3,2,0)
		Parity_1 = PAR_1.read_float(24,3,2,0)
		Stopbit_1 = PAR_1.read_float(26,3,2,0)
	
		
		print("\n"*50)
		print("Sensor Data--------------------------------")
		print(f"PAR intensity is: {PAR_intensity_1} umol.m^-2")
		print(f"slaveid={slave_1}, Baud={Baud_1}, Parit={Parity_1}, Stopbit={Stopbit_1}")

		print("------------------------------------------")
		
		print("")
		print("")
		print("")
		sleep(1)
	
	
except KeyboardInterrupt:
	
	# Piece of mind close out
	PAR_1.serial.close()
	print("Ports Now Closed")
