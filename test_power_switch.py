__author__ = 'mmoisen'
import sys
import time

from models import Heater
pin = sys.argv[1]

heater = Heater(pin=pin)

heater.turn_on()


heaters = [Heater(pin=pin) for pin in sys.argv[1:]]
[heater.turn_on() for heater in heaters]

try:
    while True:
        for heater in heaters:
            print "Heater {} is on: {}".format(heater.pin, heater.is_on)
        print ""
        time.sleep(5)
except KeyboardInterrupt:
    [heater.turn_off() for heater in heaters]
    heater.turn_off()