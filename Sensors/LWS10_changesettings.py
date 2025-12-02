import minimalmodbus

SM_600_1 = minimalmodbus.Instrument('/dev/ttyUSB0', 1)  # current slave address (likely 1)

SM_600_1.serial.baudrate = 9600
SM_600_1.serial.bytesize = 8
SM_600_1.serial.parity   = minimalmodbus.serial.PARITY_NONE
SM_600_1.serial.stopbits = 1
SM_600_1.serial.timeout  = 0.5
SM_600_1.mode = minimalmodbus.MODE_RTU

SM_600_1.clear_buffers_before_each_transaction = True
SM_600_1.close_port_after_each_call = True
