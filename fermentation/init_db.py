__author__ = 'mmoisen'

import peewee
from settings import db

from fermentation import FermentationHost, FermentationFermentor, FermentationFermwrap, FermentationProbe, \
    FermentationTemperature, FermentationSchedule

db.connect()

tables = [FermentationSchedule,
          FermentationTemperature,
          FermentationProbe,
          FermentationFermwrap,
          FermentationFermentor,
          FermentationHost]

for table in tables:
    db.drop_table(table, True)

tables.reverse()

for table in tables:
    db.create_table(table)

hostnames = 'mmoisen-WS','raspberrpy','raspberrypy1'

hosts = [FermentationHost.create(hostname=hostname) for hostname in hostnames]

fermwrap_pins = [17,18,22,23,24,25]

for host in hosts:
    [FermentationFermwrap.create(pin=pin, host=host) for pin in fermwrap_pins]

