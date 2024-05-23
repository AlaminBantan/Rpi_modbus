import minimalmodbus # Don't forget to import the library!!
from time import sleep


Solar_13 = minimalmodbus.Instrument('/dev/ttyUSB0', 13, debug=False)
Solar_13.serial.baudrate = 19200
Solar_13.serial.bytesize = 8					# Number of data bits to be requested
Solar_13.serial.parity = minimalmodbus.serial.PARITY_EVEN	# Parity Setting here is NONE but can be ODD or EVEN
Solar_13.serial.stopbits = 1					# Number of stop bits
Solar_13.serial.timeout  = 0.5					# Timeout time in seconds
Solar_13.mode = minimalmodbus.MODE_RTU			


# Good practice to clean up before and after each execution
Solar_13.clear_buffers_before_each_transaction = True
Solar_13.close_port_after_each_call = True


try:
	while True:
		
		# ~ read_float(registeraddress: int, functioncode: int = 3, number_of_registers: int = 2, byteorder: int = 0) 
		Solar_Radiation_13 = Solar_13.read_float(0, 3, 2, 0)
		slave_13 = Solar_13.read_float(16,3,2,0)
		Baud_13 = Solar_13.read_float(22,3,2,0)
		Parity_13 = Solar_13.read_float(24,3,2,0)
		Stopbit_13 = Solar_13.read_float(26,3,2,0)
	
		
		print("\n"*50)
		print("Sensor Data--------------------------------")
		print(f"Solar radiation is: {Solar_Radiation_13} W.m^-2")
		print(f"slaveid={slave_13}, Baud={Baud_13}, Parit={Parity_13}, Stopbit={Stopbit_13}")

		print("------------------------------------------")
		
		print("")
		print("")
		print("")
		sleep(1)
	
except KeyboardInterrupt:
	
	# Piece of mind close out
	Solar_13.serial.close()
	print("Ports Now Closed")

