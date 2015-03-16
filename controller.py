__author__ = 'mmoisen'

from bottle import Bottle, route, run, template, debug, post, request
from datetime import datetime, timedelta
import os

app = Bottle()


from fermentation.fermentation_controller import *

@app.route('/hai')
def hai():
    print "haiii'"

@app.route('/angular')
def angular_test():
    variables = {'first_name':'Obama',
                 'last_name':'Huessein'}

    return template('angular_test', variables)

#for Bootstrap
@app.route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')


if __name__ == '__main__':
    print "controller main lol"

    debug(True)

    run(app, host='0.0.0.0', port='8000', reloader=True)

    print "hello"