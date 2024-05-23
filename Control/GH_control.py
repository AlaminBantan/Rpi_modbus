import RPi.GPIO as GPIO
from datetime import datetime, time
import threading
import time as t

# Define GPIO channels
channel_fan1 = 25 #connect the set 1 of fans from zone B and C to relay1 (147,179)
channel_fan2 = 24 #connect the set 2 of fans from zone B and C to relay2 (148,180)
channel_mist = 23 #connect the misting pump to relay 3 (221)
channel_shade_ret = 18 #connect the shade retraction motor from zones B and C to relay 4 (125,158)
channel_shade_ex = 15 #connect the shade extension motor from zones B and C to relay 5 (126,159)
channel_pump = 14 #connect the wet pad pump from zones B and C to relay 6 (129,152)

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(channel_mist, GPIO.OUT)
GPIO.setup(channel_fan1, GPIO.OUT)
GPIO.setup(channel_fan2, GPIO.OUT)
GPIO.setup(channel_pump, GPIO.OUT)
GPIO.setup(channel_shade_ex, GPIO.OUT)
GPIO.setup(channel_shade_ret, GPIO.OUT)

# Define functions for each device

#mist
def mist_off(pin):
    GPIO.output(pin, GPIO.HIGH)
def mist_on(pin):
    GPIO.output(pin, GPIO.LOW)

#fan1
def fan1_off(pin):
    GPIO.output(pin, GPIO.HIGH)
def fan1_on(pin):
    GPIO.output(pin, GPIO.LOW)

#fan2
def fan2_off(pin):
    GPIO.output(pin, GPIO.HIGH)
def fan2_on(pin):
    GPIO.output(pin, GPIO.LOW)

#wet pad pump
def pump_off(pin):
    GPIO.output(pin, GPIO.HIGH)
def pump_on(pin):
    GPIO.output(pin, GPIO.LOW)

#shade will not be controlled by the Pi, but in case we want to we can change these lines.

#shade extension
#def shade_ex_off(pin):
#    GPIO.output(pin, GPIO.HIGH)
#def shade_ex_on(pin):
#    GPIO.output(pin, GPIO.LOW)

#shade retraction
#def shade_ret_off(pin):
#    GPIO.output(pin, GPIO.HIGH)
#def shade_ret_on(pin):
#    GPIO.output(pin, GPIO.LOW)




#########################################################################################################################
#Schedule:
    #9:00 fan2 and wet pad pump on.
    #10:00 misting starts (first mist 8 seconds to repressurize the lines) and every 20 mins one mist for 5 seconds
    #fan1 goes off 9 second before mist and go on 20 second after the mist ends.
    #fan2 goes off 7 second before mist and go on 22 second after the mist ends.
    #16:00 last misting.
    #20:00 fan2 and wet pad pump go off.
    #fan1 is on all day long (except misting intervals).
#########################################################################################################################



# Define functions to control devices in threads

#fans are delayed by 2 seconds to prevent electricl surge
def fan1_thread():
    while True:
        current_time = datetime.now().time()
        fan1_time_ranges = [
            (time(0, 0, 0), time(9, 59, 51)),
            (time(10, 0, 28), time(10, 19, 51)),
            (time(10, 20, 25), time(10, 39, 51)),
            (time(10, 40, 25), time(10, 59, 51)),
            (time(11, 0, 25), time(11, 19, 51)),
            (time(11, 20, 25), time(11, 39, 51)),
            (time(11, 40, 25), time(11, 59, 51)),
            (time(12, 0, 25), time(12, 19, 51)),
            (time(12, 20, 25), time(12, 39, 51)),
            (time(12, 40, 25), time(12, 59, 51)),
            (time(13, 0, 25), time(13, 19, 51)),
            (time(13, 20, 25), time(13, 39, 51)),
            (time(13, 40, 25), time(13, 59, 51)),
            (time(14, 0, 25), time(14, 19, 51)),
            (time(14, 20, 25), time(14, 39, 51)),
            (time(14, 40, 25), time(14, 59, 51)),
            (time(15, 0, 25), time(15, 19, 51)),
            (time(15, 20, 25), time(15, 39, 51)),
            (time(15, 40, 25), time(15, 59, 51)),
            (time(16, 0, 25), time(23, 59, 59))
        ]
        fan1_time = any(fan1_start_time <= current_time <= fan1_end_time for fan1_start_time, fan1_end_time in fan1_time_ranges)

        if fan1_time:
            fan1_on(channel_fan1)
            t.sleep(0.5)
        else:
            fan1_off(channel_fan1)
            t.sleep(0.5)


def fan2_thread():
    while True:
        current_time = datetime.now().time()
        fan2_time_ranges = [
            (time(9, 0, 30), time(9, 59, 53)),
            (time(10, 0, 30), time(10, 19, 53)),
            (time(10, 20, 27), time(10, 39, 53)),
            (time(10, 40, 27), time(10, 59, 53)),
            (time(11, 0, 27), time(11, 19, 53)),
            (time(11, 20, 27), time(11, 39, 53)),
            (time(11, 40, 27), time(11, 59, 53)),
            (time(12, 0, 27), time(12, 19, 53)),
            (time(12, 20, 27), time(12, 39, 53)),
            (time(12, 40, 27), time(12, 59, 53)),
            (time(13, 0, 27), time(13, 19, 53)),
            (time(13, 20, 27), time(13, 39, 53)),
            (time(13, 40, 27), time(13, 59, 53)),
            (time(14, 0, 27), time(14, 19, 53)),
            (time(14, 20, 27), time(14, 39, 53)),
            (time(14, 40, 27), time(14, 59, 53)),
            (time(15, 0, 27), time(15, 19, 53)),
            (time(15, 20, 27), time(15, 39, 53)),
            (time(15, 40, 27), time(15, 59, 53)),
            (time(16, 0, 27), time(20, 0, 0))
        ]
        fan2_time = any(fan2_start_time <= current_time <= fan2_end_time for fan2_start_time, fan2_end_time in fan2_time_ranges)

        if fan2_time:
            fan2_on(channel_fan2)
            t.sleep(0.5)
        else:
            fan2_off(channel_fan2)
            t.sleep(0.5)

def mist_thread():
     while True:
        current_time = datetime.now().time()
        misting_time_ranges = [
            (time(10, 0, 0), time(10, 0, 8)),
            (time(10, 20, 0), time(10, 20, 5)),
            (time(10, 40, 0), time(10, 40, 5)),
            (time(11, 0, 0), time(11, 0, 5)),
            (time(11, 20, 0), time(11, 20, 5)),
            (time(11, 40, 0), time(11, 40, 5)),
            (time(12, 0, 0), time(12, 0, 5)),
            (time(12, 20, 0), time(12, 20, 5)),
            (time(12, 40, 0), time(12, 40, 5)),
            (time(13, 0, 0), time(13, 0, 5)),
            (time(13, 20, 0), time(13, 20, 5)),
            (time(13, 40, 0), time(13, 40, 5)),
            (time(14, 0, 0), time(14, 0, 5)),
            (time(14, 20, 0), time(14, 20, 5)),
            (time(14, 40, 0), time(14, 40, 5)),
            (time(15, 0, 0), time(15, 0, 5)),
            (time(15, 20, 0), time(15, 20, 5)),
            (time(15, 40, 0), time(15, 40, 5)),
            (time(16, 0, 0), time(16, 0, 5))
        ]
        misting_time = any(mist_start_time <= current_time <= mist_end_time for mist_start_time, mist_end_time in misting_time_ranges)

        if misting_time:
            print("mist is on")
            mist_on(channel_mist)
            t.sleep(0.5)
        else:
            mist_off(channel_mist)
            t.sleep(0.5)

def pump_thread():
    while True:
        current_time = datetime.now().time()

        if time(9, 0, 0) <= current_time <= time(20, 0, 0):
            pump_on(channel_pump)
            t.sleep(5)
        else:
            pump_off(channel_pump)
            t.sleep(5)
            
            
#def shade_ex_thread():
#    while True:
#        current_time = datetime.now().time()
#
#       if time(10, 30) <= current_time <= time(10, 33):
#            shade_ex_on(channel_shade_ex)
#        else:
#            shade_ex_off(channel_shade_ex)

#def shade_ret_thread():
#    while True:
#        current_time = datetime.now().time()
#
#       if time(1, 30) <= current_time <= time(1, 33):
#            shade_ret_on(channel_shade_ret)
#        else:
#            shade_ret_off(channel_shade_ret)


try:
    # Start threads for each device
    threading.Thread(target=mist_thread).start()
    threading.Thread(target=fan1_thread).start()
    threading.Thread(target=fan2_thread).start()
    threading.Thread(target=pump_thread).start()
    # threading.Thread(target=shade_ex_thread).start()
    # threading.Thread(target=shade_ret_thread).start()

    # Keep the main thread running
    while True:
        pass

except KeyboardInterrupt:
    GPIO.cleanup()
