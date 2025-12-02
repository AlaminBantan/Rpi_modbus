import minimalmodbus

LW_1 = minimalmodbus.Instrument('/dev/ttyUSB0', 1)  # current slave address (likely 1)

LW_1.serial.baudrate = 9600
LW_1.serial.bytesize = 8
LW_1.serial.parity   = minimalmodbus.serial.PARITY_NONE
LW_1.serial.stopbits = 1
LW_1.serial.timeout  = 0.5
LW_1.mode = minimalmodbus.MODE_RTU

LW_1.clear_buffers_before_each_transaction = True
LW_1.close_port_after_each_call = True

# Change BAUDRATE to 19200 (value 4 at register 513)
LW_1.write_register(513, 4, functioncode=6)   # BAUDRATE 19200 bps

# Ensure protocol is RTU (0)
LW_1.write_register(514, 0, functioncode=6)   # PROTOCOL Modbus RTU

# Parity: 1 = Even
LW_1.write_register(515, 1, functioncode=6)   # PARITY Even

# Data bits: 1 = 8 bits
LW_1.write_register(516, 1, functioncode=6)   # DATABITS 8 bits

# Stop bits: 0 = 1 stop bit
LW_1.write_register(517, 0, functioncode=6)   # STOPBITS 1 stop bit

# OPTIONAL: change slave address (if you want, otherwise skip)
LW_1.write_register(512, 10, functioncode=6)   # SLAVEADDRESS = 10
