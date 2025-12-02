import minimalmodbus

PH_1 = minimalmodbus.Instrument('/dev/ttyUSB0', 1)  # known working ID

PH_1.serial.baudrate = 9600
PH_1.serial.bytesize = 8
PH_1.serial.parity   = minimalmodbus.serial.PARITY_NONE
PH_1.serial.stopbits = 1
PH_1.serial.timeout  = 0.5
PH_1.mode = minimalmodbus.MODE_RTU

PH_1.clear_buffers_before_each_transaction = True
PH_1.close_port_after_each_call = True

print("Scanning registers 0-199 with FC3...")

for addr in range(0, 200):
    try:
        val = PH_1.read_register(addr, 0, functioncode=3, signed=False)
    except Exception as e:
        # If something goes wrong on a specific address, just skip it
        print(f"{addr:3d}: ERROR ({e})")
        continue

    line = f"{addr:3d}: {val:5d}"

    # Heuristic highlighting: possible ID or baud-code candidates
    if 1 <= val <= 247:
        line += "   <- possible ID candidate"
    if 1 <= val <= 6:
        line += "   <- possible baud-code candidate"

    print(line)
