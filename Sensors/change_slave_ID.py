import minimalmodbus  # Don't forget to import the library!!
from time import sleep

# Make an "instrument" object called SM_600_1 (port name, slave address (in decimal))
SM_600_1 = minimalmodbus.Instrument('/dev/ttyACM0', 1, debug=False)

SM_600_1.serial.baudrate = 19200                             # BaudRate
SM_600_1.serial.bytesize = 8                                 # Number of data bits to be requested
SM_600_1.serial.parity = minimalmodbus.serial.PARITY_EVEN    # Parity Setting is EVEN
SM_600_1.serial.stopbits = 1                                 # Number of stop bits
SM_600_1.mode = minimalmodbus.MODE_RTU                       # Mode to be used (RTU or ascii mode)

# Good practice to clean up before and after each execution
SM_600_1.clear_buffers_before_each_transaction = True
SM_600_1.close_port_after_each_call = True



#write_register(registeraddress: int, value: Union[int, float], number_of_decimals: int = 0, functioncode: int = 16, signed: bool = False) → None

SM_600_1.write_register(120,4, 0, 16, False)





