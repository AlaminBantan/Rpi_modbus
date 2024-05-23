import minimalmodbus # Don't forget to import the library!!
from time import sleep

#configuration of SP-522 ID=11
Solar_11 = minimalmodbus.Instrument('/dev/ttyACM0', 11, debug=False)
Solar_11.serial.baudrate = 19200 	
Solar_11.serial.bytesize = 8					# Number of data bits to be requested
Solar_11.serial.parity = minimalmodbus.serial.PARITY_NONE	# Parity Setting here is NONE but can be ODD or EVEN
Solar_11.serial.stopbits = 1					# Number of stop bits
Solar_11.serial.timeout  = 0.5					# Timeout time in seconds
Solar_11.mode = minimalmodbus.MODE_RTU			
Solar_11.clear_buffers_before_each_transaction = True
Solar_11.close_port_after_each_call = True

#configuration of SP-522 ID=12
Solar_12 = minimalmodbus.Instrument('/dev/ttyACM0', 12, debug=False)
Solar_12.serial.baudrate = 19200 	
Solar_12.serial.bytesize = 8					# Number of data bits to be requested
Solar_12.serial.parity = minimalmodbus.serial.PARITY_NONE	# Parity Setting here is NONE but can be ODD or EVEN
Solar_12.serial.stopbits = 1					# Number of stop bits
Solar_12.serial.timeout  = 0.5					# Timeout time in seconds
Solar_12.mode = minimalmodbus.MODE_RTU			
Solar_12.clear_buffers_before_each_transaction = True
Solar_12.close_port_after_each_call = True

#configuration of SP-522 ID=13
Solar_13 = minimalmodbus.Instrument('/dev/ttyACM0', 13, debug=False)
Solar_13.serial.baudrate = 19200 	
Solar_13.serial.bytesize = 8					# Number of data bits to be requested
Solar_13.serial.parity = minimalmodbus.serial.PARITY_NONE	# Parity Setting here is NONE but can be ODD or EVEN
Solar_13.serial.stopbits = 1					# Number of stop bits
Solar_13.serial.timeout  = 0.5					# Timeout time in seconds
Solar_13.mode = minimalmodbus.MODE_RTU			
Solar_13.clear_buffers_before_each_transaction = True
Solar_13.close_port_after_each_call = True

#configuration of SP-522 ID=14
Solar_14 = minimalmodbus.Instrument('/dev/ttyACM0', 14, debug=False)
Solar_14.serial.baudrate = 19200 	
Solar_14.serial.bytesize = 8					# Number of data bits to be requested
Solar_14.serial.parity = minimalmodbus.serial.PARITY_NONE	# Parity Setting here is NONE but can be ODD or EVEN
Solar_14.serial.stopbits = 1					# Number of stop bits
Solar_14.serial.timeout  = 0.5					# Timeout time in seconds
Solar_14.mode = minimalmodbus.MODE_RTU			
Solar_14.clear_buffers_before_each_transaction = True
Solar_14.close_port_after_each_call = True

#configuration of SQ-618 ID=1
PAR_1 = minimalmodbus.Instrument('/dev/ttyACM0',1)	# Make an "instrument" object called PAR_1 (port name, slave address (in decimal))
PAR_1.serial.baudrate = 19200 	
PAR_1.serial.bytesize = 8					# Number of data bits to be requested
PAR_1.serial.parity = minimalmodbus.serial.PARITY_NONE	# Parity Setting here is NONE but can be ODD or EVEN
PAR_1.serial.stopbits = 1					# Number of stop bits
PAR_1.serial.timeout  = 0.5					# Timeout time in seconds
PAR_1.mode = minimalmodbus.MODE_RTU				# Mode to be used (RTU or ascii mode)
PAR_1.clear_buffers_before_each_transaction = True
PAR_1.close_port_after_each_call = True

#configuration of SQ-618 ID=2
PAR_2 = minimalmodbus.Instrument('/dev/ttyACM0',2)	
PAR_2.serial.baudrate = 19200 				# BaudRate
PAR_2.serial.bytesize = 8					# Number of data bits to be requested
PAR_2.serial.parity = minimalmodbus.serial.PARITY_NONE	# Parity Setting here is NONE but can be ODD or EVEN
PAR_2.serial.stopbits = 1					# Number of stop bits
PAR_2.serial.timeout  = 0.5					# Timeout time in seconds
PAR_2.mode = minimalmodbus.MODE_RTU				# Mode to be used (RTU or ascii mode)
PAR_2.clear_buffers_before_each_transaction = True
PAR_2.close_port_after_each_call = True

#configuration of SQ-618 ID=3
PAR_3 = minimalmodbus.Instrument('/dev/ttyACM0',3)	
PAR_3.serial.baudrate = 19300 				# BaudRate
PAR_3.serial.bytesize = 8					# Number of data bits to be requested
PAR_3.serial.parity = minimalmodbus.serial.PARITY_NONE	# Parity Setting here is NONE but can be ODD or EVEN
PAR_3.serial.stopbits = 1					# Number of stop bits
PAR_3.serial.timeout  = 0.5					# Timeout time in seconds
PAR_3.mode = minimalmodbus.MODE_RTU				# Mode to be used (RTU or ascii mode)
PAR_3.clear_buffers_before_each_transaction = True
PAR_3.close_port_after_each_call = True

#configuration of SQ-618 ID=4
PAR_4 = minimalmodbus.Instrument('/dev/ttyACM0',4)	
PAR_4.serial.baudrate = 19400 				# BaudRate
PAR_4.serial.bytesize = 8					# Number of data bits to be requested
PAR_4.serial.parity = minimalmodbus.serial.PARITY_NONE	# Parity Setting here is NONE but can be ODD or EVEN
PAR_4.serial.stopbits = 1					# Number of stop bits
PAR_4.serial.timeout  = 0.5					# Timeout time in seconds
PAR_4.mode = minimalmodbus.MODE_RTU				# Mode to be used (RTU or ascii mode)
PAR_4.clear_buffers_before_each_transaction = True
PAR_4.close_port_after_each_call = True

# Configuration of GMP-252 ID=41
carbo_41 = minimalmodbus.Instrument('/dev/ttyACM0',41)
carbo_41.serial.baudrate = 19200
carbo_41.serial.bytesize = 8
carbo_41.serial.parity = minimalmodbus.serial.PARITY_NONE
carbo_41.serial.stopbits = 2
carbo_41.mode = minimalmodbus.MODE_RTU
carbo_41.clear_buffers_before_each_transaction = True
carbo_41.close_port_after_each_call = True

# Configuration of GMP-252 ID=42
carbo_42 = minimalmodbus.Instrument('/dev/ttyACM0',42)
carbo_42.serial.baudrate = 19200
carbo_42.serial.bytesize = 8
carbo_42.serial.parity = minimalmodbus.serial.PARITY_NONE
carbo_42.serial.stopbits = 2
carbo_42.mode = minimalmodbus.MODE_RTU
carbo_42.clear_buffers_before_each_transaction = True
carbo_42.close_port_after_each_call = True

try:
	while True:
		
		# ~ read_float(registeraddress: int, functioncode: int = 3, number_of_registers: int = 2, byteorder: int = 0) 
		Solar_Radiation_11 = Solar_11.read_float(0, 3, 2, 0)
		slave_11 = Solar_11.read_float(16,3,2,0)
		Baud_11 = Solar_11.read_float(22,3,2,0)
		Parity_11 = Solar_11.read_float(24,3,2,0)
		Stopbit_11 = Solar_11.read_float(26,3,2,0)
	
		
		print("\n"*50)
		print("Sensor Data--------------------------------")
		print(f"Solar radiation is: {Solar_Radiation_11} W.m^-2")
		print(f"slaveid={slave_11}, Baud={Baud_11}, Parit={Parity_11}, Stopbit={Stopbit_11}")

		print("------------------------------------------")
		
		print("")
		print("")
		print("")
		sleep(1)
	
except KeyboardInterrupt:
	
	# Piece of mind close out
	Solar_11.serial.close()
	print("Port 11 Now Closed")


try:
	while True:
		
		# ~ read_float(registeraddress: int, functioncode: int = 3, number_of_registers: int = 2, byteorder: int = 0) 
		Solar_Radiation_12 = Solar_12.read_float(0, 3, 2, 0)
		slave_12 = Solar_12.read_float(16,3,2,0)
		Baud_12 = Solar_12.read_float(22,3,2,0)
		Parity_12 = Solar_12.read_float(24,3,2,0)
		Stopbit_12 = Solar_12.read_float(26,3,2,0)
	
		
		print("\n"*50)
		print("Sensor Data--------------------------------")
		print(f"Solar radiation is: {Solar_Radiation_12} W.m^-2")
		print(f"slaveid={slave_12}, Baud={Baud_12}, Parit={Parity_12}, Stopbit={Stopbit_12}")

		print("------------------------------------------")
		
		print("")
		print("")
		print("")
		sleep(1)
	
except KeyboardInterrupt:
	
	# Piece of mind close out
	Solar_12.serial.close()
	print("Port 12 Now Closed")

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
	print("Port 13 Now Closed")
try:
	while True:
		
		# ~ read_float(registeraddress: int, functioncode: int = 3, number_of_registers: int = 2, byteorder: int = 0) 
		Solar_Radiation_14 = Solar_14.read_float(0, 3, 2, 0)
		slave_14 = Solar_14.read_float(16,3,2,0)
		Baud_14 = Solar_14.read_float(22,3,2,0)
		Parity_14 = Solar_14.read_float(24,3,2,0)
		Stopbit_14 = Solar_14.read_float(26,3,2,0)
	
		
		print("\n"*50)
		print("Sensor Data--------------------------------")
		print(f"Solar radiation is: {Solar_Radiation_14} W.m^-2")
		print(f"slaveid={slave_14}, Baud={Baud_14}, Parit={Parity_14}, Stopbit={Stopbit_14}")

		print("------------------------------------------")
		
		print("")
		print("")
		print("")
		sleep(1)
	
except KeyboardInterrupt:
	
	# Piece of mind close out
	Solar_14.serial.close()
	print("Port 14 Now Closed")

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
	print("Port 1 Now Closed")



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
	print("Port 2 Now Closed")


try:
	while True:
		
		# ~ read_float(registeraddress: int, functioncode: int = 3, number_of_registers: int = 2, byteorder: int = 0) 
		PAR_intensity_3 = PAR_3.read_float(0, 3, 2, 0)
		slave_3 = PAR_3.read_float(16,3,2,0)
		Baud_3 = PAR_3.read_float(22,3,2,0)
		Parity_3 = PAR_3.read_float(24,3,2,0)
		Stopbit_3 = PAR_3.read_float(26,3,2,0)
	
		
		print("\n"*50)
		print("Sensor Data--------------------------------")
		print(f"PAR intensity is: {PAR_intensity_3} umol.m^-2")
		print(f"slaveid={slave_3}, Baud={Baud_3}, Parit={Parity_3}, Stopbit={Stopbit_3}")

		print("------------------------------------------")
		
		print("")
		print("")
		print("")
		sleep(1)
	
except KeyboardInterrupt:
	
	# Piece of mind close out
	PAR_3.serial.close()
	print("Port 3 Now Closed")

try:
	while True:
		
		# ~ read_float(registeraddress: int, functioncode: int = 3, number_of_registers: int = 2, byteorder: int = 0) 
		PAR_intensity_4 = PAR_4.read_float(0, 3, 2, 0)
		slave_4 = PAR_4.read_float(16,3,2,0)
		Baud_4 = PAR_4.read_float(22,3,2,0)
		Parity_4 = PAR_4.read_float(24,3,2,0)
		Stopbit_4 = PAR_4.read_float(26,3,2,0)
	
		
		print("\n"*50)
		print("Sensor Data--------------------------------")
		print(f"PAR intensity is: {PAR_intensity_4} umol.m^-2")
		print(f"slaveid={slave_4}, Baud={Baud_4}, Parit={Parity_4}, Stopbit={Stopbit_4}")

		print("------------------------------------------")
		
		print("")
		print("")
		print("")
		sleep(1)
	
except KeyboardInterrupt:
	
	# Piece of mind close out
	PAR_4.serial.close()
	print("Port 4 Now Closed")


try:
	while True:
		
		# ~ read_float(registeraddress: int, functioncode: int = 3, number_of_registers: int = 2, byteorder: int = 0) 
		carbon_conc_41 = carbo_41.read_float(1, 3, 2, 0)
			
		
		print("\n"*50)
		print("Sensor Data--------------------------------")
		print(f"CO2 concentration 41 is: {carbon_conc_41} ppm")
		print("------------------------------------------")
		sleep(10)
	
except KeyboardInterrupt:
	
	# Piece of mind close out
	carbo_41.serial.close()
	print("Port 41 Now Closed")

try:
	while True:
		
		# ~ read_float(registeraddress: int, functioncode: int = 3, number_of_registers: int = 2, byteorder: int = 0) 
		carbon_conc_42 = carbo_42.read_float(1, 3, 2, 0)
			
		
		print("\n"*50)
		print("Sensor Data--------------------------------")
		print(f"CO2 concentration 42 is: {carbon_conc_41} ppm")
		print("------------------------------------------")
		sleep(10)
	
except KeyboardInterrupt:
	
	# Piece of mind close out
	carbo_42.serial.close()
	print("Port  42 Now Closed")