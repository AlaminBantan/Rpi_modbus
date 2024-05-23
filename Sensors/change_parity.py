import minimalmodbus # Don't forget to import the library!!
from time import sleep

PAR_1 = minimalmodbus.Instrument('/dev/ttyACM0',1)	# Make an "instrument" object called PAR_1 (port name, slave address (in decimal))

PAR_1.serial.baudrate = 19200 	
PAR_1.serial.bytesize = 8					# Number of data bits to be requested
PAR_1.serial.parity = minimalmodbus.serial.PARITY_EVEN	# Parity Setting here is NONE but can be ODD or EVEN
PAR_1.serial.stopbits = 1					# Number of stop bits
PAR_1.serial.timeout  = 0.5					# Timeout time in seconds
PAR_1.mode = minimalmodbus.MODE_RTU				# Mode to be used (RTU or ascii mode)

# Good practice to clean up before and after each execution
PAR_1.clear_buffers_before_each_transaction = True
PAR_1.close_port_after_each_call = True


#write_register(registeraddress: int, value: Union[int, float], number_of_decimals: int = 0, functioncode: int = 16, signed: bool = False) → None
PAR_1.write_register(52,0, 0, 16, False)