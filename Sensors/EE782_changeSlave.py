#!/usr/bin/env python3
"""
Change Modbus slave address on EE872 (or similar) using minimalmodbus.

- Talks to the device at CURRENT_ID
- Writes NEW_ID to holding register 1 using FC=0x06
- Verifies by reading a known register at NEW_ID

Edit CURRENT_ID and NEW_ID below, then run.
"""

import sys
import time
import minimalmodbus

# --------- EDIT THESE TWO ---------
CURRENT_ID = 211   # existing/slave address you can currently communicate with
NEW_ID     = 111   # desired new slave address (1..247)
# ----------------------------------

# (Optional) port and serial setup — match what you already use
PORT = "/dev/ttyACM0"
BAUD = 19200
BYTESIZE = 8
PARITY = minimalmodbus.serial.PARITY_NONE
STOPBITS = 1
TIMEOUT_S = 1.0

# A simple, reliable register to read for verification (int ppm)
# (These worked for you earlier; adjust if needed)
REG_CO2_AVG_INT = 0xFBE  # 4030 dec — CO2 avg (int), FC=4

def make_instr(addr: int) -> minimalmodbus.Instrument:
    instr = minimalmodbus.Instrument(PORT, addr, debug=False)
    instr.serial.baudrate = BAUD
    instr.serial.bytesize = BYTESIZE
    instr.serial.parity   = PARITY
    instr.serial.stopbits = STOPBITS
    instr.serial.timeout  = TIMEOUT_S
    instr.mode = minimalmodbus.MODE_RTU
    instr.clear_buffers_before_each_transaction = True
    instr.close_port_after_each_call = True
    return instr

def main():
    if not (1 <= NEW_ID <= 247):
        print(f"NEW_ID {NEW_ID} is out of valid Modbus range (1..247).")
        sys.exit(1)
    if CURRENT_ID == NEW_ID:
        print("CURRENT_ID and NEW_ID are the same — nothing to change.")
        sys.exit(0)

    print(f"Attempting to change Modbus address from {CURRENT_ID} to {NEW_ID}...")

    # 1) Talk to current address
    instr = make_instr(CURRENT_ID)

    # Optional: quick sanity check that we can read something first
    try:
        _ = instr.read_register(REG_CO2_AVG_INT, functioncode=4, signed=True)
        print(f"✓ Communication OK at CURRENT_ID={CURRENT_ID}")
    except Exception as e:
        print(f"✗ Could not communicate with CURRENT_ID={CURRENT_ID}: {e}")
        sys.exit(1)

    # 2) Write NEW_ID to parameter "Modbus address" at register 1 (dec) via FC=6
    try:
        # write_register(registeraddress, value, number_of_decimals=0, functioncode=16)
        # For single register write with FC=6, pass functioncode=6
        instr.write_register(1, NEW_ID, number_of_decimals=0, functioncode=6, signed=False)
        print(f"✓ Wrote NEW_ID={NEW_ID} to register 1 using FC=0x06")
    except Exception as e:
        print(f"✗ Failed to write new address: {e}")
        sys.exit(1)

    # Some devices need a brief pause (or power-cycle). Try a short delay first.
    time.sleep(0.5)

    # 3) Verify by talking to the new address
    new_instr = make_instr(NEW_ID)
    try:
        val = new_instr.read_register(REG_CO2_AVG_INT, functioncode=4, signed=True)
        print(f"✓ Verification success at NEW_ID={NEW_ID}. CO2 AVG int read: {val} ppm")
        print("Address change complete.")
    except Exception as e:
        print("! Could not verify at the new address right away.")
        print("  Some devices require a reboot/power-cycle after address change.")
        print(f"  Error when trying NEW_ID={NEW_ID}: {e}")
        print("  Try power-cycling the sensor, then test communication at the new address.")

if __name__ == "__main__":
    main()
