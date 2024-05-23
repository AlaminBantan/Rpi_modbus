import minimalmodbus
import struct

def configure_instrument(port, address):
    instrument = minimalmodbus.Instrument(port, address)
    instrument.serial.baudrate = 9600  
    instrument.serial.bytesize = 8  
    instrument.serial.parity = minimalmodbus.serial.PARITY_NONE  
    instrument.serial.stopbits = 1  
    instrument.mode = minimalmodbus.MODE_RTU
    instrument.clear_buffers_before_each_transaction = True
    instrument.close_port_after_each_call = True
    return instrument

def construct_modbus_request(address, start_register, num_registers, crc_check):
    # Convert values to bytes
    address_byte = bytes([address])
    function_byte = bytes([0x04])
    start_register_bytes = start_register.to_bytes(2, byteorder='big')
    num_registers_bytes = num_registers.to_bytes(2, byteorder='big')
    crc_bytes = crc_check.to_bytes(2, byteorder='big')

    # Construct the request
    request = address_byte + function_byte + start_register_bytes + num_registers_bytes + crc_bytes

    return request

if __name__ == "__main__":
    # Configure your Modbus instrument
    port = '/dev/ttyACM0'  # Example port, change it to your actual port
    address = 0  # Address of the Modbus device

    try:
        # Configure Modbus instrument
        instrument = configure_instrument(port, address)

        # Start register address
        start_register_address = 0x0000  # Start register address

        # Number of registers to read
        num_registers_to_read = 3  # We are reading registers 0x0000 to 0x0002

        # CRC check value
        crc_check_value = 0xB00B

        # Construct Modbus request
        request = construct_modbus_request(address, start_register_address, num_registers_to_read, crc_check_value)

        # Send request and read response
        response = instrument._perform_command(4, request)
        
        # Extract register values from the response
        register_values = struct.unpack('>' + 'h' * num_registers_to_read, response[3:-2])
        
        # Print the register values
        print("Register values:", register_values)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        # Close the Modbus instrument
        instrument.serial.close()
