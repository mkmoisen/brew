__author__ = 'mmoisen'

import peewee
from settings import db

from fermentation.fermentation import FermentationHost, FermentationFermentor, FermentationFermwrap, FermentationProbe, \
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
