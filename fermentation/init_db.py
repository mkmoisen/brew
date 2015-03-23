__author__ = 'mmoisen'

import peewee
from settings import db

from fermentation import FermentationHost, FermentationFermentor, FermentationFermwrap, FermentationProbe, \
    FermentationTemperature, FermentationSchedule

import os
from settings import BREW_PROPERTIES_FILE


tables = [FermentationSchedule,
          FermentationTemperature,
          FermentationProbe,
          FermentationFermwrap,
          FermentationFermentor,
          FermentationHost]


def drop_and_create_tables():

    db.connect()

    print "dropping tables"
    for table in tables:
        db.drop_table(table, True)

    tables.reverse()

    # This creates indexes and foreign keys
    print "creating tables"
    db.create_tables(tables)

    '''
    My GoDaddy MYSQL database's default engine is MyISAM which doesn't support transactions or FKs
    However this command will only work on MySQL and will break on other DBs
    '''

    print "changing tables to innodb"
    for table in tables:
        db.execute_sql("ALTER TABLE {} ENGINE = InnoDB".format(table._meta.db_table))

    ''' calling db.create_table on a single table doesn't create indexes or foreign keys!'''
    #for table in tables:
    #    db.create_table(table)
    #    table.
    #    table.create_indexes()

    hostnames = 'mmoisen-WS','raspberrpy','raspberrypy1'

    print "creating hosts"
    hosts = [FermentationHost.create(hostname=hostname) for hostname in hostnames]

    fermwrap_pins = [17,18,22,23,24,25]

    print "creating fermwraps"
    for host in hosts:
        [FermentationFermwrap.create(pin=pin, host=host) for pin in fermwrap_pins]

    db.close()

def drop_brew_properties():
    os.remove(BREW_PROPERTIES_FILE)