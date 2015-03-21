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

# This creates indexes and foreign keys
db.create_tables(tables)

''' calling db.create_table on a single table doesn't create indexes or foreign keys!'''
#for table in tables:
#    db.create_table(table)
#    table.
#    table.create_indexes()

hostnames = 'mmoisen-WS','raspberrpy','raspberrypy1'

hosts = [FermentationHost.create(hostname=hostname) for hostname in hostnames]

fermwrap_pins = [17,18,22,23,24,25]

for host in hosts:
    [FermentationFermwrap.create(pin=pin, host=host) for pin in fermwrap_pins]

