#!/usr/bin/env python3
import time
from gpiozero import OutputDevice

# BCM pin numbers
PINS = [22, 27, 17]

# Active-high relays? Set False if your board is active-low
ACTIVE_HIGH = False

# Initialize devices
devices = [OutputDevice(pin, active_high=ACTIVE_HIGH, initial_value=False) for pin in PINS]

try:
    print("🔌 Turning ALL relays ON (Ctrl+C to stop)")
    for dev, pin in zip(devices, PINS):
        dev.on()
        print(f"➡️ Pin {pin} ON")

    # Keep running until user stops it
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\n🛑 Stopping test, turning everything OFF")
    for dev in devices:
        dev.off()
