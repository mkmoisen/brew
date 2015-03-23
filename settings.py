__author__ = 'mmoisen'

import peewee

#MYSQL_USERNAME='username'
#MYSQL_DATABASE='database'
#MYSQL_PASSWORD='password'
#MYSQL_HOST='host'

'''
todo:
change this to a database proxy to use different dbs
'''

BREW_PROPERTIES_FILE = "brew.properties"

hostnames = ['raspberrypi','raspberrypi1']

try:
    from local_settings import *
except ImportError:
    print "Create a 'local_settings.py' file (or edit settings.py) containing the following constants:\nMYSQL_USERNAME=''\nMYSQL_HOST=''\nMYSQL_PASSWORD=''\nMYSQL_DATABASE=''\n"

db = peewee.MySQLDatabase(MYSQL_DATABASE,user=MYSQL_USERNAME, host=MYSQL_HOST,passwd=MYSQL_PASSWORD)

def get_db():
    db.connect()
    db.get_conn().ping(True)
    return db

class BaseModel(peewee.Model):
    class Meta:
        database = db
