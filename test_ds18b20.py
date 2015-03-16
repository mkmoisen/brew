__author__ = 'mmoisen'

import sys
import time
import os

from models import Probe

if len(sys.argv) == 1:
    probes = [Probe('hlt', file) for file in os.listdir(Probe.BASE_DIR) if file != 'w1_bus_master1']
else:
    probes = [Probe('hlt', file) for file in sys.argv[1:]]

while True:
    for probe in probes:
        print "{} temperature is {}".format(probe.file_name, probe.temp)
    time.sleep(5)