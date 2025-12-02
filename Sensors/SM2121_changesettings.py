import minimalmodbus

ph = minimalmodbus.Instrument('/dev/ttyUSB0', 1)  # current ID = 1
ph.serial.baudrate = 9600
ph.serial.bytesize = 8
ph.serial.parity   = minimalmodbus.serial.PARITY_NONE
ph.serial.stopbits = 1
ph.serial.timeout  = 0.5
ph.mode = minimalmodbus.MODE_RTU

ph.clear_buffers_before_each_transaction = True
ph.close_port_after_each_call = True

# 1️⃣ Change baud rate to 19200 (code 4) at register 103
ph.write_register(103, 4, functioncode=6)

# 2️⃣ Change device ID to 21 at register 102
ph.write_register(102, 21, functioncode=6)

print("Changed baud to 19200 and address to 21. Update your serial settings accordingly.")
