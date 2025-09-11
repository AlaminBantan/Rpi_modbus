#!/usr/bin/env python3
import time
from gpiozero import OutputDevice

# BCM pin numbers
PINS = [22, 27, 17]

# Active-high relays? Set False if your board is active-low
ACTIVE_HIGH = False

# Duration in seconds
ON_TIME = 5
OFF_TIME = 5

# Initialize devices
devices = [OutputDevice(pin, active_high=ACTIVE_HIGH, initial_value=False) for pin in PINS]

try:
    print("🔄 Starting pin cycle test (Ctrl+C to stop)")
    while True:
        for dev, pin in zip(devices, PINS):
            print(f"➡️ Pin {pin} ON")
            dev.on()
            time.sleep(ON_TIME)

            print(f"➡️ Pin {pin} OFF")
            dev.off()
            time.sleep(OFF_TIME)

except KeyboardInterrupt:
    print("\n🛑 Stopping test, turning everything OFF")
    for dev in devices:
        dev.off()
