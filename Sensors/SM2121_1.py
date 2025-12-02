import minimalmodbus

PH_1 = minimalmodbus.Instrument('/dev/ttyUSB0', 1)

PH_1.serial.baudrate = 9600
PH_1.serial.bytesize = 8
PH_1.serial.parity   = minimalmodbus.serial.PARITY_NONE
PH_1.serial.stopbits = 1
PH_1.serial.timeout  = 0.5
PH_1.mode = minimalmodbus.MODE_RTU

PH_1.clear_buffers_before_each_transaction = True
PH_1.close_port_after_each_call = True

# Read pH just to confirm comms
ph_raw = PH_1.read_register(0, 0, functioncode=3, signed=False)
print("pH raw:", ph_raw, "->", ph_raw / 100.0)

print("Config registers 100–105 (FC3):")
for addr in range(100, 106):
    val = PH_1.read_register(addr, 0, functioncode=3, signed=False)
    print(addr, ":", val)
