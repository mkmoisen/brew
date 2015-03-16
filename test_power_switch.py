__author__ = 'mmoisen'
import sys
import time

from models import Heater
pin = sys.argv[1]

heater = Heater(pin=pin)

heater.turn_on()


try:
    while True:
        print "Heater is on: {}".format(heater.is_on)
        time.sleep(5)
except KeyboardInterrupt:
    heater.turn_off()