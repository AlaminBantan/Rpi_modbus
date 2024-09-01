import RPi.GPIO as GPIO

# Setup GPIO
RELAY_PIN = 17  # Use the GPIO pin you have connected the relay to
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

# Turn off the relay
GPIO.output(RELAY_PIN, GPIO.LOW)

# Cleanup GPIO
GPIO.cleanup()
