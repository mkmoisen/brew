__author__ = 'mmoisen'


from bottle import Bottle, route, run, template, debug, post, request
from datetime import datetime, timedelta
import os

import sys

app = Bottle()

from fermentation.init_db import drop_and_create_tables, drop_brew_properties



@app.route('/hai')
def hai():
    print "haiii'"

@app.route('/angular')
def angular_test():
    variables = {'first_name':'Obama',
                 'last_name':'Huessein'}

    return template('angular_test', variables)

from fermentation.fermentation import FermentationHost, FermentationFermentor, FermentationProbe, FermentationFermwrap, \
    FermentationTemperature, FermentationSchedule

tables = [FermentationHost, FermentationFermentor, FermentationProbe, FermentationFermwrap, \
    FermentationTemperature, FermentationSchedule]

for table in tables:
    table._meta.db_table += '_t'

#get_db().create_tables(tables, True)


if len(sys.argv) > 1:
    print "len is > 1"
    print "arg is ", sys.argv[1]
    if sys.argv[1].lower() == 'drop':
        drop_and_create_tables()
        try:
            drop_brew_properties()
        except:
            pass

#for Bootstrap
@app.route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')


if __name__ == '__main__':
    from fermentation.fermentation_controller import *

    print "controller main lol"

    debug(True)

    run(app, host='0.0.0.0', port='8000', reloader=True)

    print "hello"