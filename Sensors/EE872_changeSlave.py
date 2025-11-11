import minimalmodbus
from time import sleep

# --- edit these ---
CURRENT_ID = 211        # current slave address
NEW_ID     = 112        # new slave address (1..247)
PORT       = '/dev/ttyACM0'
# -------------------

inst = minimalmodbus.Instrument(PORT, CURRENT_ID, debug=False)

inst.serial.baudrate = 19200
inst.serial.bytesize = 8
inst.serial.parity   = minimalmodbus.serial.PARITY_NONE  # change to PARITY_NONE if your bus uses N-8-1
inst.serial.stopbits = 1
inst.mode = minimalmodbus.MODE_RTU

inst.clear_buffers_before_each_transaction = True
inst.close_port_after_each_call = True

# Write Single Register (FC=6): holding register 1 = NEW_ID
# write_register(registeraddress, value, number_of_decimals=0, functioncode=6, signed=False)
inst.write_register(1, NEW_ID, 0, 6, False)

# tiny pause; some devices apply immediately, others need power-cycle
sleep(0.2)
