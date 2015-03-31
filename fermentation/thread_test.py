__author__ = 'mmoisen'

import threading
import time
import json

class API(object):
    updated = False

    @classmethod
    def listen(cls):
        time.sleep(10)
        cls.updated = True
'''
t = threading.Thread(name="api", target=API.listen)

i = 0
t.start()
while not API.updated:
    print i, "updated = ", API.updated
    i+=1
    time.sleep(1)
'''


from bottle import Bottle, route, run, template, debug, post, request
from datetime import datetime, timedelta
import os

thread_app = Bottle()
debug(True)

@thread_app.post('/update/')
@thread_app.post('/update')
def update():
    post = json.loads(request.forms.dict.keys()[0])
    print post
    print "type post = ",type(post)

    if post['updated']:
        API.updated = True
    return json.dumps({'lol':1})



t = threading.Thread(name="api", target=run, args=(thread_app,), kwargs={'host':'0.0.0.0','port':'8010'})

i=0
t.start()
t = None

while not API.updated:
    print i, "updated = ", API.updated
    i+=1
    time.sleep(1)

print "Updated!"

class MyThread(threading.Thread):
    def __init__(self, target, *args):
        threading.Thread.__init__(self, target=target, args=args)