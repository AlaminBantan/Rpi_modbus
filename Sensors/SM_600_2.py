import minimalmodbus  # Don't forget to import the library!!
from time import sleep

# Make an "instrument" object called SM_600_2 (port name, slave address (in decimal))
SM_600_2 = minimalmodbus.Instrument('/dev/ttyACM0', 2, debug=False)

SM_600_2.serial.baudrate = 19200                             # BaudRate
SM_600_2.serial.bytesize = 8                                 # Number of data bits to be requested
SM_600_2.serial.parity = minimalmodbus.serial.PARITY_EVEN    # Parity Setting is EVEN
SM_600_2.serial.stopbits = 1                                 # Number of stop bits
SM_600_2.mode = minimalmodbus.MODE_RTU                       # Mode to be used (RTU or ascii mode)

# Good practice to clean up before and after each execution
SM_600_2.clear_buffers_before_each_transaction = True
SM_600_2.close_port_after_each_call = True

# Register map (holding registers), float32 big-endian (MSB first)
# PAR: 0, Temp: 2, RH: 4, CO2: 6, Pressure: 8, VPD: 10, Dew Point: 12, Fan RPM: 14

try:
    while True:
        # read_float(registeraddress: int, functioncode: int = 3, number_of_registers: int = 2, byteorder: int = 0)
        # byteorder=0 -> Big-Endian (most significant byte sent first)
        par       = SM_600_2.read_float(0, 3, 2, 0)
        temp_c    = SM_600_2.read_float(2, 3, 2, 0)
        rh_pct    = SM_600_2.read_float(4, 3, 2, 0)
        co2_ppm   = SM_600_2.read_float(6, 3, 2, 0)
        pressure  = SM_600_2.read_float(8, 3, 2, 0)
        vpd_kpa   = SM_600_2.read_float(10, 3, 2, 0)
        dewpoint  = SM_600_2.read_float(12, 3, 2, 0)
        fanrpm  = SM_600_2.read_float(14, 3, 2, 0)

        print("\n" * 50)
        print("SM-600 Sensor Data--------------------------------")
        print(f"PAR         : {par:.2f} µmol m^-2 s^-1")
        print(f"Temperature : {temp_c:.2f} °C")
        print(f"RH          : {rh_pct:.2f} %")
        print(f"CO₂         : {co2_ppm:.2f} ppm")
        print(f"Pressure    : {pressure:.2f} kPa")
        print(f"VPD         : {vpd_kpa:.3f} kPa")
        print(f"Dew Point   : {dewpoint:.2f} °C")
        print(f"Fan RPM   : {fanrpm:.2f} rpm")
        print("-----------------------------------------------")
        sleep(10)

except KeyboardInterrupt:
    # Peace of mind close out
    try:
        SM_600_2.serial.close()
    except Exception:
        pass
    print("Ports Now Closed")
