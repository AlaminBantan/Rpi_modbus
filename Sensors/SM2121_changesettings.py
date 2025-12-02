import minimalmodbus

# Talk to pH sensor with its CURRENT settings
ph = minimalmodbus.Instrument('/dev/ttyUSB0', 1)  # current address = 1

ph.serial.baudrate = 9600        # or 19200 if you already changed it
ph.serial.bytesize = 8
ph.serial.parity   = minimalmodbus.serial.PARITY_NONE
ph.serial.stopbits = 1
ph.serial.timeout  = 0.5
ph.mode = minimalmodbus.MODE_RTU

ph.clear_buffers_before_each_transaction = True
ph.close_port_after_each_call = True

# OPTIONAL: set baud rate to 19200 (code 4) if not already done
ph.write_register(103, 4, functioncode=6)   # register 103 = 0x0067

# Change device address to 21 at register 102 (0x0066)
ph.write_register(102, 21, functioncode=6)

print("Done: baud set to 19200 (code 4), address set to 21.")
