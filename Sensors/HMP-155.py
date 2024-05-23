import serial
import io
from time import sleep

def read_device(serial_wrapper, device_number):
    try:
        # Open the device
        serial_wrapper.write(f"OPEN {device_number}\r\n")
        serial_wrapper.flush()
        print(f"Device {device_number} is opened")
        sleep(5)

        # Send the data request
        serial_wrapper.write("SEND\r\n")
        serial_wrapper.flush()
        print("Send")
        sleep(10)

        # Read and print the data
        data = serial_wrapper.readlines()
        print(f"Data from Device {device_number}: {data}")
        sleep(3)

    finally:
        # Close the device
        serial_wrapper.write("CLOSE\r\n")
        serial_wrapper.flush()
        print(f"Device {device_number} closed")
        sleep(5)

# Define device numbers in a circular manner
device_numbers = ["31", "32", "33", "34"]

# Serial configuration for all devices
serial_devices = [serial.Serial("/dev/ttyACM1",
                                baudrate=4800,
                                bytesize=serial.SEVENBITS,
                                parity=serial.PARITY_EVEN,
                                stopbits=serial.STOPBITS_ONE,
                                xonxoff=False,
                                timeout=2) for _ in range(len(device_numbers))]

# TextIOWrapper objects for all devices
THUM_devices = [io.TextIOWrapper(io.BufferedRWPair(serial_device, serial_device)) for serial_device in serial_devices]

try:
    while True:
        for i, device_number in enumerate(device_numbers):
            read_device(THUM_devices[i], device_number)

except KeyboardInterrupt:
    # Clean up when interrupted
    print("Ports Now Closed")
finally:
    # Close all open ports
    for serial_device in serial_devices:
        serial_device.close()
