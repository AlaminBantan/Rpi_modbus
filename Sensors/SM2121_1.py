import minimalmodbus

ph = minimalmodbus.Instrument('/dev/ttyUSB0', 1)  # same as your working reader

# EXACT same serial config as your working pH reader
ph.serial.baudrate = 9600
ph.serial.bytesize = 8
ph.serial.parity   = minimalmodbus.serial.PARITY_NONE
ph.serial.stopbits = 1
ph.serial.timeout  = 0.5
ph.mode = minimalmodbus.MODE_RTU

ph.clear_buffers_before_each_transaction = True
ph.close_port_after_each_call = True

# ---- TEST READS ONLY ----
# 1) Read pH register (0) to confirm comms
ph_raw = ph.read_register(0, 0, functioncode=3, signed=False)
print("Test pH raw:", ph_raw, "->", ph_raw/100.0, "pH")

# 2) Read baud-code register 103 (should be 3 for 9600 by default)
baud_code = ph.read_register(103, 0, functioncode=3, signed=False)
print("Current baud code at reg 103:", baud_code)
