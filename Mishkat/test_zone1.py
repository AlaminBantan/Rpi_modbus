#!/usr/bin/env python3
import time
from gpiozero import OutputDevice

# --- Pins (BCM numbering) ---
PUMP_PIN = 17
Z1_PIN   = 27
ACTIVE_HIGH = True   # set False if your relays are active-LOW

# --- Timing ---
PUMP_LEAD = 1.0      # pump starts this many seconds before valve
MIST_DUR  = 10       # valve open seconds
PUMP_LAG  = 2.0      # pump keeps running after valve closes

# --- Devices ---
pump = OutputDevice(PUMP_PIN, active_high=ACTIVE_HIGH, initial_value=False)
z1   = OutputDevice(Z1_PIN,   active_high=ACTIVE_HIGH, initial_value=False)

try:
    print("💧 Test Zone 1: starting pump + valve sequence")

    # Pump lead
    pump.on()
    time.sleep(PUMP_LEAD)

    # Open valve
    z1.on()
    print("Valve Z1 ON")
    time.sleep(MIST_DUR)

    # Close valve
    z1.off()
    print("Valve Z1 OFF")

    # Pump lag
    time.sleep(PUMP_LAG)
    pump.off()
    print("Pump OFF")

    print("✅ Test finished")

except KeyboardInterrupt:
    print("Interrupted — closing everything")
    z1.off(); pump.off()
