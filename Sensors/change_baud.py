import minimalmodbus
from time import sleep

id = 13
time_it = 10
c = 0
n_inst = minimalmodbus.Instrument('/dev/ttyUSB0', id, debug=False)  # port name, slave address (in decimal)
n_inst.serial.baudrate = 9600


n_inst.write_register(51,3,0,16, False)