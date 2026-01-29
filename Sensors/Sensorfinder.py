#!/usr/bin/env python3
"""
Comprehensive sensor finder - tries different slave IDs and serial settings
"""

import minimalmodbus
import serial
from time import sleep

PORT = "/dev/ttyACM0"  # Change this if your USB adapter is on a different port

print("=" * 70)
print("COMPREHENSIVE SENSOR SCANNER")
print("=" * 70)
print()
print(f"Scanning on port: {PORT}")
print()
print("This will try:")
print("  - Slave IDs: 1 to 50")
print("  - Different baud rates: 9600, 19200, 38400")
print("  - Different parity: None, Even, Odd")
print("  - Different stop bits: 1, 2")
print("  - Different registers: 0, 1, 256")
print()
input("Press Enter to start scanning...")
print()

# Check if port exists
import os
if not os.path.exists(PORT):
    print(f"ERROR: Port {PORT} does not exist!")
    print()
    print("Available ports:")
    import glob
    for p in glob.glob('/dev/ttyACM*') + glob.glob('/dev/ttyUSB*'):
        print(f"  {p}")
    print()
    print("Edit the script to change PORT variable to the correct device.")
    exit(1)

found_sensors = []

# Serial settings combinations to try
settings_to_try = [
    (19200, serial.PARITY_EVEN, 1, "19200-8E1"),
    (19200, serial.PARITY_NONE, 2, "19200-8N2"),
    (19200, serial.PARITY_NONE, 1, "19200-8N1"),
    (19200, serial.PARITY_ODD, 1, "19200-8O1"),
    (9600, serial.PARITY_EVEN, 1, "9600-8E1"),
    (9600, serial.PARITY_NONE, 1, "9600-8N1"),
    (38400, serial.PARITY_EVEN, 1, "38400-8E1"),
    (38400, serial.PARITY_NONE, 1, "38400-8N1"),
]

# Registers to try reading
registers_to_try = [
    (0, "register 0"),
    (1, "register 1"),
    (256, "register 256"),
]

total_combinations = 50 * len(settings_to_try) * len(registers_to_try)
current = 0

print("Scanning... (this may take a few minutes)")
print()

for slave_id in range(1, 51):
    for baud, parity, stopbits, desc in settings_to_try:
        for reg, reg_desc in registers_to_try:
            current += 1
            
            # Show progress every 100 attempts
            if current % 100 == 0:
                percent = (current / total_combinations) * 100
                print(f"Progress: {percent:.1f}% ({current}/{total_combinations})", flush=True)
            
            try:
                inst = minimalmodbus.Instrument(PORT, slave_id)
                inst.serial.baudrate = baud
                inst.serial.bytesize = 8
                inst.serial.parity = parity
                inst.serial.stopbits = stopbits
                inst.serial.timeout = 0.3
                inst.mode = minimalmodbus.MODE_RTU
                inst.clear_buffers_before_each_transaction = True
                inst.close_port_after_each_call = True
                
                # Try reading as float
                try:
                    value = inst.read_float(reg, 3, 2, 0)
                    found_sensors.append({
                        'id': slave_id,
                        'settings': desc,
                        'register': reg_desc,
                        'value': value,
                        'type': 'float'
                    })
                    print(f"\nFOUND: ID {slave_id}, {desc}, {reg_desc}, float value: {value:.2f}")
                    # Don't break - keep checking for more ways to read this sensor
                except:
                    pass
                
            except:
                pass
            
            sleep(0.01)  # Small delay to not overwhelm the bus

print()
print("=" * 70)
print("SCAN COMPLETE")
print("=" * 70)
print()

if found_sensors:
    print(f"Found {len(found_sensors)} sensor response(s):")
    print()
    
    # Group by slave ID
    sensors_by_id = {}
    for sensor in found_sensors:
        if sensor['id'] not in sensors_by_id:
            sensors_by_id[sensor['id']] = []
        sensors_by_id[sensor['id']].append(sensor)
    
    for slave_id in sorted(sensors_by_id.keys()):
        print(f"Slave ID {slave_id}:")
        for sensor in sensors_by_id[slave_id]:
            print(f"  Settings: {sensor['settings']}")
            print(f"  Register: {sensor['register']}")
            print(f"  Value: {sensor['value']:.2f} ({sensor['type']})")
            print()
    
    print("=" * 70)
    print("RECOMMENDED CONFIGURATION:")
    print("=" * 70)
    
    # Show config for the first found sensor
    first = found_sensors[0]
    print(f"""
inst = minimalmodbus.Instrument('{PORT}', {first['id']})
inst.serial.baudrate = {settings_to_try[[s[3] for s in settings_to_try].index(first['settings'])][0]}
inst.serial.bytesize = 8
inst.serial.parity = serial.PARITY_{first['settings'].split('-')[1][1]}
inst.serial.stopbits = {settings_to_try[[s[3] for s in settings_to_try].index(first['settings'])][2]}
inst.serial.timeout = 1.0
inst.mode = minimalmodbus.MODE_RTU
inst.clear_buffers_before_each_transaction = True
inst.close_port_after_each_call = True

# Read value
value = inst.read_float({first['register']}, 3, 2, 0)
""")
    
else:
    print("No sensors found!")
    print()
    print("Possible issues:")
    print("  1. Sensor not powered")
    print("  2. Wrong port (check with: ls -la /dev/tty*)")
    print("  3. RS-485 adapter not connected properly")
    print("  4. Sensor has unusual settings not covered by this scan")
    print("  5. Sensor is damaged")
    print()
    print("Try:")
    print("  - Check power LED on sensor")
    print("  - Check RS-485 wiring (A, B, GND)")
    print("  - Verify USB adapter is detected: ls -la /dev/ttyACM* /dev/ttyUSB*")

print("=" * 70)
