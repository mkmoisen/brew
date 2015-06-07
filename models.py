__author__ = 'mmoisen'

from abc import ABCMeta
import time

try:
    import RPi.GPIO as io
    io.setmode(io.BCM)
except ImportError:
    print "run this on the RPi"

class Probe(object):
    BASE_DIR = '/sys/bus/w1/devices/'
    RETRY_MAX = 5

    def __init__(self, probe_type, file_name):
        if not probe_type in ("mashtun","hlt","wort","ambient", "swamp"):
            raise ValueError('probe_type must be in ("mashtun","hlt","wort","ambient","swamp")')
        self.probe_type = probe_type
        self.file_name = file_name
        self.retry_count = 0
        if file_name is None:
            return

        device_folder = Probe.BASE_DIR + file_name
        self.device_file = device_folder + '/w1_slave'

    def read_temp_raw(self):
        with open(self.device_file, 'r') as f:
            return f.readlines()

    @property
    def temp(self):
        if self.file_name is None:
            # Account for testing or lack of ambient/swamp probe
            return None
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            if self.retry_count < Probe.RETRY_MAX:
                self.retry_count += 1
                time.sleep(5) # Is this bad ?
                lines = self.read_temp_raw()
            else:
                raise RuntimeError("Probe {} is malfunctioning. 25 seconds of retrying failed!".format(self.file_name))
        self.retry_count = 0
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            if temp_f == 185.0:
                raise RuntimeError("Probe {} is 185.0F!".format(self.file_name))
            return temp_f

    def __str__(self):
        return "probe_type = {}, file_name = {}".format(self.probe_type, self.file_name)

    def __repr__(self):
        return "Probe(probe_type='{}', file_name='{}')".format(self.probe_type, self.file_name)




class PowerSwitchTail2():
    __metaclass__ = ABCMeta

    def __init__(self, pin):
        self.pin = int(pin)
        self.is_on = False
        io.setup(self.pin, io.OUT)
        self.turn_off()

    def turn_on(self):
        io.output(self.pin, True)
        self.is_on = True

    def turn_off(self):
        io.output(self.pin, False)
        self.is_on = False

    def __str__(self):
        return "pin = {}".format(self.pin)

    def __repr__(self):
        return "{}(pin={})".format(self.__class__.__name__, self.pin)

class Pump(PowerSwitchTail2):
    pass

class Heater(PowerSwitchTail2):
    pass
