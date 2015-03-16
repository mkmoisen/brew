__author__ = 'mmoisen'

import sys
import time
import os

from models import Probe



def probes():
    if len(sys.argv) == 1:
        probes = [Probe('hlt', file) for file in os.listdir(Probe.BASE_DIR) if file != 'w1_bus_master1']
    else:
        probes = [Probe('hlt', file) for file in sys.argv[1:]]

    return probes

while True:
    for probe in probes():
        try:
            print "{} temperature is {}".format(probe.file_name, probe.temp)
        except Exception as ex:
            print "Error reading {}: ".format(probe.file_name), ex.__class__.__name__, ex.message
    time.sleep(5)