#!/usr/bin/env python3
# change_slave_address.py
# Minimal script to change a device's Modbus slave address via register 1 (FC=6).

import time
import argparse
import minimalmodbus

def make_instr(port, addr, baud, timeout, parity, stopbits, bytesize):
    inst = minimalmodbus.Instrument(port, addr, debug=False)
    inst.serial.baudrate = baud
    inst.serial.timeout  = timeout
    inst.serial.parity   = parity
    inst.serial.stopbits = stopbits
    inst.serial.bytesize = bytesize
    inst.mode = minimalmodbus.MODE_RTU
    inst.clear_buffers_before_each_transaction = True
    inst.close_port_after_each_call = True
    return inst

def main():
    ap = argparse.ArgumentParser(description="Change Modbus slave address (writes holding register 1 with FC=6).")
    ap.add_argument("--port", default="/dev/ttyACM0")
    ap.add_argument("--current", type=int, required=True, help="Current slave address (1..247)")
    ap.add_argument("--new", type=int, required=True, dest="new_id", help="New slave address (1..247)")
    ap.add_argument("--baud", type=int, default=19200)
    ap.add_argument("--timeout", type=float, default=1.0)
    ap.add_argument("--verify", action="store_true", help="After writing, try reading a register at the new address")
    ap.add_argument("--verify-reg", type=lambda x: int(x, 0), default=0xFBE, help="Register to read for verify (default 0xFBE)")
    ap.add_argument("--verify-fc", type=int, default=4, help="Function code for verify read (default 4)")
    ap.add_argument("--parity", choices=["N", "E", "O"], default="N")
    ap.add_argument("--stopbits", type=int, choices=[1,2], default=1)
    ap.add_argument("--bytesize", type=int, choices=[7,8], default=8)
    args = ap.parse_args()

    if not (1 <= args.current <= 247 and 1 <= args.new_id <= 247):
        print("ERROR: Addresses must be in 1..247.")
        return
    if args.current == args.new_id:
        print("INFO: Current and new address are the same; nothing to do.")
        return

    parity_map = {
        "N": minimalmodbus.serial.PARITY_NONE,
        "E": minimalmodbus.serial.PARITY_EVEN,
        "O": minimalmodbus.serial.PARITY_ODD
    }

    print("Writing new address...")
    inst = make_instr(args.port, args.current, args.baud, args.timeout, parity_map[args.parity], args.stopbits, args.bytesize)

    try:
        # Write Single Register (FC=6): holding register 1 <- new address
        inst.write_register(1, args.new_id, number_of_decimals=0, functioncode=6, signed=False)
        print("OK: Wrote new address %d to register 1 using FC=6." % args.new_id)
    except Exception as e:
        print("ERROR: Write failed: %s" % e)
        return

    # Short pause; some devices need a moment (others need power-cycle)
    time.sleep(0.5)

    if args.verify:
        print("Verifying at new address %d..." % args.new_id)
        new_inst = make_instr(args.port, args.new_id, args.baud, args.timeout, parity_map[args.parity], args.stopbits, args.bytesize)
        try:
            val = new_inst.read_register(args.verify_reg, functioncode=args.verify_fc, signed=True)
            print("OK: Verify read succeeded at new address. Register 0x%X = %d" % (args.verify_reg, val))
        except Exception as e:
            print("WARN: Could not verify immediately at new address: %s" % e)
            print("      If the device doesn’t respond, power-cycle it and try again.")

if __name__ == "__main__":
    main()
