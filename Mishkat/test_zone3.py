#!/usr/bin/env python3
import time
from gpiozero import OutputDevice

# --- Pins (BCM numbering) ---
PUMP_PIN = 17
Z3_PIN   = 22
ACTIVE_HIGH = True   # set False if your relays are active-LOW

# --- Timing ---
PUMP_LEAD = 1.0
MIST_DUR  = 10
PUMP_LAG  = 2.0

# --- Devices ---
pump = OutputDevice(PUMP_PIN, active_high=ACTIVE_HIGH, initial_value=False)
z3   = OutputDevice(Z3_PIN,   active_high=ACTIVE_HIGH, initial_value=False)

try:
    print("💧 Test Zone 3: starting pump + valve sequence")

    pump.on()
    time.sleep(PUMP_LEAD)

    z3.on()
    print("Valve Z3 ON")
    time.sleep(MIST_DUR)

    z3.off()
    print("Valve Z3 OFF")

    time.sleep(PUMP_LAG)
    pump.off()
    print("Pump OFF")

    print("✅ Test finished")

except KeyboardInterrupt:
    print("Interrupted — closing everything")
    z3.off(); pump.off()
