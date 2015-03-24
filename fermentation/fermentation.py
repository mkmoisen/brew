__author__ = 'mmoisen'

import peewee
import json
import socket

from models import Probe, Heater
from settings import BaseModel, get_db, BREW_PROPERTIES_FILE

import traceback
import sys

try:
    import RPi.GPIO as io
    io.setmode(io.BCM)
except ImportError:
    print "run this on the RPi"

from datetime import datetime, timedelta

import time


class FermentationHost(BaseModel):
    hostname = peewee.CharField(unique=True, max_length=50)
    updated = peewee.IntegerField(default=0, choices=((0,0),(1,1))) # Either 0 or 1

    class Meta:
        db_table = 'fermentation_host'

class FermentationFermentor(BaseModel):
    name = peewee.CharField(max_length=255)
    start_date = peewee.DateField()
    end_begin_date = peewee.DateField(null=True)
    end_end_date = peewee.DateField(null=True)
    yeast = peewee.CharField(max_length=225, null=True)
    og = peewee.DoubleField(null=True)
    fg = peewee.DoubleField(null=True)
    start_temp = peewee.DoubleField()
    temp_differential = peewee.DoubleField(default=0.125)
    active = peewee.IntegerField(default=1, choices=((0,0),(1,1))) # Either 0 or 1
    material = peewee.CharField(max_length=50, choices =(('Glass','Glass'),('Plastic','Plastic'),('Metal','Metal')))
    host = peewee.ForeignKeyField(FermentationHost, related_name="host_fermentors")

    class Meta:
        db_table = 'fermentation_fermentor'

class FermentationFermwrap(BaseModel):
    pin = peewee.IntegerField(default=17, choices=tuple([(k,k) for k in [17,18,22,23,24,25]]))
    in_use = peewee.IntegerField(default=0, choices=((0,0),(1,1))) # What is this for?
    is_on = peewee.IntegerField(default=0, choices=((0,0),(1,1)))
    host = peewee.ForeignKeyField(FermentationHost, related_name="host_fermwraps")
    fermentor = peewee.ForeignKeyField(FermentationFermentor, related_name="fermentor_fermwraps", null=True)

    class Meta:
        db_table = 'fermentation_fermwrap'
        indexes = (
            # Unique Key = True
            (('host','pin'),True),
        )

class FermentationProbe(BaseModel):
    file_name = peewee.CharField(max_length=50)
    type = peewee.CharField(max_length=50, choices= tuple([(k.lower(),k) for k in ['Wort','Ambient', 'Swamp']]))
    in_use = peewee.IntegerField(default=0, choices=((0,0),(1,1)))
    host = peewee.ForeignKeyField(FermentationHost, related_name="host_probes")
    fermentor = peewee.ForeignKeyField(FermentationFermentor, related_name="fermentor_probes")

    class Meta:
        db_table = 'fermentation_probe'
        #Fermentors commonly share the ambient probe noob
        indexes = (
            (('host','fermentor','type'),True),
        )


class FermentationTemperature(BaseModel):
    fermentor = peewee.ForeignKeyField(FermentationFermentor, related_name="fermentor_temperatures")
    dt = peewee.DateTimeField()
    ambient_temp = peewee.DoubleField(null=True)
    wort_temp = peewee.DoubleField()
    swamp_cooler_temp = peewee.DoubleField(null=True)

    class Meta:
        db_table = 'fermentation_temperature'
        indexes = (
            (('fermentor','dt'), False),
            (('dt','fermentor'), False),
        )

class FermentationSchedule(BaseModel):
    fermentor = peewee.ForeignKeyField(FermentationFermentor, related_name="fermentor_schedules")
    dt = peewee.DateTimeField()
    temp = peewee.DoubleField()

    class Meta:
        db_table = 'fermentation_schedule'
        indexes = (
            # Unique Key = True
            (('fermentor','dt'), True),
        )


class FermentorIter(type):
    '''
    A static class can not become an iterable via the __iter__() method.
    To make a static class an iterable, you have to add an __iter__() method
    to a metaclass that the static class will use.

    To let a static class use len() on it, __len__ must likewise be defined in the meta class
    '''
    def __iter__(cls):
        for fermentor in FermentorList.fermentors:
            yield fermentor

    def __len__(cls):
        return len(cls.fermentors)

class FermentorList(object):
    '''
    This is a static class that is iterable.
    This replaces the fermentor_list array and obviates the need to append
    each fermentor object to the fermentor_list array.
    The Fermentor __init__() method must cal FermentorList.append(self) for this to work.
    '''

    __metaclass__ = FermentorIter

    fermentors = []

    @classmethod
    def append(cls, fermentor):
        if isinstance(fermentor, Fermentor):
            cls.fermentors.append(fermentor)
        else:
            raise TypeError("FermentorList.append only accepts type Fermentor. Received type {}".format(type(fermentor)))

    @classmethod
    def clear(cls):
        cls.fermentors = []

    @classmethod
    def turn_fermwraps_off(cls):
        for fermentor in cls:
            if fermentor.is_fermwrap:
                fermentor.turn_fermwrap_off()



class ScheduleIncrease(object):
    def __init__(self, dt=None, temp=None):
        '''
        init expects either:
            ScheduleIncrease(date='2015-01-01 00:00:00', 68)
        or
            ScheduleIncrease(t=('2015-01-01 00:00:00', 68))
        '''
        if type(dt) == str or type(dt) == unicode:
            self.dt = datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S')
        elif type(dt) == datetime:
            self.dt = dt
        else:
            raise TypeError('dt needs to be str or datetime, not {}'.format(type(dt)))

        self.temp = temp

    def __gt__(self, other):
        if self.dt > other.dt:
            return True
        return False

    def __eq__(self, other):
        if self.dt == other.dt:
            return True
        return False

    def __str__(self):
        return 'ScheduleIncrease(dt={}, temp={})'.format(self.dt, self.temp)
    def __repr__(self):
        return str(self)

class Schedule(object):
    '''
    This class documents any temperature rests, like Diacyl rests and lagering, the Fermentor should under go.

    The trick here is that I don't have anything to measure specific gravity. I can only make decisions based
    off time. If I normally raise temperatures on ales 72 hours in, but a particular batch is having a sluggish
    fermentation, I should be able to tell the app to delay its rise. Likewise if a particular batch is having
    a tremendous fermentation, I should be able to tell the app to increase early.
    '''

    # replace this with def__init__(self, start_temp, increases):
    def __init__(self, start_date, start_temp, increases):
        '''

        :param start_date: Day the beer was pitched
        :param increases: a list containing tuples of (hours, temperature)
            for example, if an ale starting at 68*F should be increased by 1*F after 3 days,
            1*F after 4 days, and 1*F after 5 days:
Schedule('2015-01-01 00:00:00', 68, [(72,69),
                        (96, 70),
                        (120, 71)])
            If a Lager should utilize the Brulosophy Quick Lager Method of
            After 5 days at 50*F, increase by 5*F every 12 hours until 65*F, hold for 5 days, then drop 5*F
            every 12 hours until 35*F:
Schedule('2015-01-01 00:00:00', 50, [(5*24, 55),
                            (5*24 + 12, 60),
                            (5*24 + 24, 65),
                            (5*24 + 24 + 5*24, 55),
                            (5*24 + 24 + 5*24 + 12, 50),
                            (5*24 + 24 + 5*24 + 12*2, 55),
                            (5*24 + 24 + 5*24 + 12*3, 50),
                            (5*24 + 24 + 5*24 + 12*4, 45),
                            (5*24 + 24 + 5*24 + 12*5, 40),
                            (5*24 + 24 + 5*24 + 12*6, 35),])
        :return:
        '''
        if type(start_date) == str or type(start_date) == unicode:
            self.start_date = datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S')
        elif type(start_date) == datetime:
            self.start_date = start_date
        else:
            raise TypeError("start_date must be a datetime.datetime object. start_date was {}".format(type(start_date)))
        self.start_temp = start_temp
        self.increases = []
        ''' Add the proper datetime to the ScheduleIncrease depending on the fermentor's start_date'''
        ''' This is stupid it should be date times inputted into the UI not hours noob '''
        # TODO: Change this to dt instead of hours
        # TODO: If end user says temp should increase 5 degrees in 12 hours,
        # TODO: I should divide 5/12 = 0.41*F/hr and then add new increases appropriately
        #for increase in increases:
        #    increase.dt = self.start_date + timedelta(hours=increase.hours)
        #    self.increases.append(increase)
        # Should I sort by date time ascending here as a sanity check? Probably
        self.increases = increases

        # Add start date/temp as first schedule

        #self.increases.insert(0, ScheduleIncrease(dt=self.start_date, temp=self.start_temp))
        self.increases.sort(key=lambda increase:increase.dt)

        computed_increases = []

        previous = ScheduleIncrease(dt=self.start_date, temp=self.start_temp)

        for i in xrange(len(self.increases)):

            '''
            # Original
            if i == len(self.increases) - 1:
                temp_difference = current.temp - previous.temp
                time_difference = (current.dt - previous.dt).total_seconds() / 60 / 60
                print "time diff between {} and {} is {}".format(current.dt, previous.dt, time_difference)
            else:
                next = self.increases[i+1]
                temp_difference = next.temp - current.temp
                time_difference = (next.dt - current.dt).total_seconds() / 60 / 60 #This this to be int
                print "time diff between {} and {} is {}".format(next.dt, current.dt, time_difference)
            '''

            '''
            # Second try using previous for temp and time difference
            current = self.increases[i]
            temp_difference = current.temp - previous.temp
            time_difference = (current.dt - previous.dt).total_seconds() / 60 / 60
            print "time diff between {} and {} is {}".format(current.dt, previous.dt, time_difference)
            '''

            # Third try using previous for temp, but next for time
            current = self.increases[i]
            temp_difference = current.temp - previous.temp
            if i == len(self.increases) - 1:
                time_difference = (current.dt - previous.dt).total_seconds() / 60 / 60
                #print "time diff between {} and {} is {}".format(current.dt, previous.dt, time_difference)
            else:
                next = self.increases[i+1]
                time_difference = (next.dt - current.dt).total_seconds() / 60 / 60 #This this to be int
                #print "time diff between {} and {} is {}".format(next.dt, current.dt, time_difference)



            if time_difference > 12.0:
                time_difference = 12.0
            #print "\t",time_difference
            ratio = temp_difference/ time_difference

            time_difference = int(round(time_difference))

            # i = hours
            #for i in xrange(1, time_difference + 1):
            for i in xrange(time_difference):
                computed_increases.append(ScheduleIncrease(
                    dt = current.dt + timedelta(hours = i),
                    temp = previous.temp + ratio*(i+1)
                ))

            previous = current

        #self.increases.extend(computed_increases)
        self.increases = computed_increases
        self.increases.sort(key=lambda increase: increase.dt)



        '''
        sorted_increases = increases[:]
        sorted_increases.sort(lambda increase: increase.dt)
        assert sorted_increases == increases
        '''

    def get_current_temp(self, today=None, start_temp=None):
        '''
        The fermentor will request the current temp every 5 seconds.
        It's important to optimize this as much as possible.

        In the normal pass, this method is simply called by schedule.get_current_temp() with no args

        :param today: This is for testing purposes only
        :param start_temp: This is for unit testing only
        :return: float
        '''
        if today is None:
            today = datetime.now()

        # This is only for testing, start_temp should be set on Schedule initialization
        if not hasattr(self, 'start_temp'):
            temp = start_temp
        else:
            temp = self.start_temp

        to_pop = []
        for i in range(0, len(self.increases)):
            #print "today=",today
            #print "self.increases[i].dt=",self.increases[i]
            if i != len(self.increases) - 1:
                #print "self.increases[i+1]=",self.increases[i+1]
                pass
            # today > self.increases[len(self.increases) - 1].dt
            if i == len(self.increases) - 1:
                #print "last in array i=",i,self.increases[i]
                if today >= self.increases[i].dt:
                    temp = self.increases[i].temp
                    break
                else:
                    raise RuntimeError("NOOOB NOT POSSIBLE IF ARRAY ORDERED CORRECTLY!")
            # today < self.increases[0]
            elif i == 0 and today < self.increases[i].dt and today < self.increases[i + 1].dt:
                    #print today, "<", self.increases[i].dt, "and", today,"<", self.increases[i + 1].dt
                    #print "today is less than first increase",self.increases[i]
                    temp = start_temp
                    break
            elif today >= self.increases[i].dt and today < self.increases[i + 1].dt:
                #print today, ">=", self.increases[i].dt, "and", today, "<", self.increases[i+1].dt
                temp = self.increases[i].temp
                break
            elif today > self.increases[i].dt and today >= self.increases[i+1].dt: ##
                #print today, ">", self.increases[i].dt, "and" ,today, ">=" ,self.increases[i+1].dt
                #print "popping ",self.increases[i]
                # remove this and the else after completion
                to_pop.append(i)
            else:
                print "NOOOOOOOOB else condition"

        if to_pop:
            #print "popping ",to_pop[0],len(to_pop), "len of increases=", len(self.increases)
            del self.increases[to_pop[0]:len(to_pop)]

        return temp


'''

from fermentation.fermentation import Schedule, ScheduleIncrease
from datetime import datetime
schedule = Schedule('2015-01-01 00:00:00', 50, [ScheduleIncrease(hours=5*24,temp=55),
                            ScheduleIncrease(hours=5*24 + 12*1,temp=60),
                            ScheduleIncrease(hours=5*24 + 12*2,temp=65),
                            ScheduleIncrease(hours=5*24 + 12*2 + 5*24,temp=60),
                            ScheduleIncrease(hours=5*24 + 12*2 + 5*24 + 12*1,temp=55),
                            ScheduleIncrease(hours=5*24 + 12*2 + 5*24 + 12*2,temp=50),
                            ScheduleIncrease(hours=5*24 + 12*2 + 5*24 + 12*3,temp=45),
                            ScheduleIncrease(hours=5*24 + 12*2 + 5*24 + 12*4,temp=40),
                            ScheduleIncrease(hours=5*24 + 12*2 + 5*24 + 12*5,temp=35),])

print schedule.increases
start_temp=0

today = '2015-01-30 00:00:00'
today = datetime.strptime(today, '%Y-%m-%dT%H:%M:%S')
print schedule.get_current_temp(today, start_temp)
print schedule.increases

for i in xrange(0, len(schedule.increases) -1):
    if today >= schedule.start_date + timedelta(hours=schedule.increases[i][0]) \
        and today <= schedule.start_date + timedelta(hours=schedule.increases[i+1][0]):
        print schedule.increases[i], schedule.start_date + timedelta(hours=schedule.increases[i][0])
        print schedule.increases[i+1], schedule.start_date + timedelta(hours=schedule.increases[i+1][0])
        print "new temp == ", schedule.increases[i+1][1]
        break

for i in xrange(0, 10):
    print i
'''
class Fermentor(object):
    def __init__(self, name=None, start_temp=None, temp_differential=None, fermwrap_pin=None, schedule=None, id=None):
        self.probes = []
        self.name = name
        self.is_disconnected = False # What is this for?
        self.is_fermwrap = False
        self.is_fermwrap_on = False
        self.start_temp = start_temp
        self.temp_differential = temp_differential
        self.schedule = schedule
        self.id = id # This is the database id from peewee

        if fermwrap_pin is not None:
            self.set_fermwrap(int(fermwrap_pin)) # Int in the event ui screws up and saves it as string

        FermentorList.append(self) # Necessary for FermentorList to be iterable

    #def __str__(self):

    def add_probe(self, probe):
        self.probes.append(probe)
        if probe.probe_type == 'wort':
            self.wort_probe = probe
        elif probe.probe_type == 'ambient':
            self.ambient_probe = probe
        elif probe.probe_type == 'swamp':
            self.swamp_probe = probe

    # I removed read_temps here to the individual probes

    def set_fermwrap(self, fermwrap_pin):
        self.fermwrap_pin = fermwrap_pin
        self.is_fermwrap = True
        io.setup(self.fermwrap_pin, io.OUT)
        io.output(self.fermwrap_pin, False)

    def turn_fermwrap_on(self):
        if self.is_fermwrap:
            #print "Turning fermwrap ON for {} as temp is < {}".format(self.name, self.min_temp)
            io.output(self.fermwrap_pin, True)
            self.is_fermwrap_on = True

            # TODO: Update Fermwrap db table here

    def turn_fermwrap_off(self, reason = None):
        if self.is_fermwrap:
            if reason == None:
                #print "Turning fermwrap OFF for {} as temp is >= to {}".format(self.name, self.max_temp)
                pass
            else:
                print "Turning fermwrap OFF for {}".format(reason)
                pass
            io.output(self.fermwrap_pin, False)
            self.is_fermwrap_on = False

            # TODO: Update Fermwrap db table here

    @property
    def min_temp(self):
        current_temp = self.schedule.get_current_temp(start_temp=self.start_temp)
        return current_temp - self.temp_differential

    @property
    def max_temp(self):
        current_temp = self.schedule.get_current_temp(start_temp=self.start_temp)
        return current_temp + self.temp_differential

    def __str__(self):
        line = 'Name: {}\n'.format(self.name)
        line += 'Temp range: {} - {}\n'.format(self.min_temp, self.max_temp)
        if self.is_fermwrap:
            line += 'Fermwrap pin: {}'.format(self.fermwrap_pin)
        else:
            line += 'I am not fermwrapped\n'
        for probe in self.probes:
            line += 'Probe {} - {}'.format(probe.probe_type, probe.file_name)
        return line










class Properties(object):
    current_poll_count = 0
    POLL_COUNT_MAX = 30

    @classmethod
    def read_properties_from_db(cls):
        '''
        The only time I should get the properties file from the DB is if I broke one raspberrypi and needed to
        get a new one up and running for previously active fermentors.
        
        The goal now is to always read properties from disk so as to not be dependent on remote godaddy mysql.
        '''
        get_db()
        query = (FermentationHost.select()
                    .where(FermentationHost.hostname==socket.gethostname())
                 .join(FermentationFermentor)
                    .where(FermentationFermentor.active == 1)
                 .join(FermentationProbe, on=FermentationProbe.fermentor)
                 .switch(FermentationFermentor)
                 .join(FermentationFermwrap, peewee.JOIN_LEFT_OUTER, on=FermentationFermwrap.fermentor)
                 .switch(FermentationFermentor)
                 .join(FermentationSchedule, peewee.JOIN_LEFT_OUTER, on=FermentationSchedule.fermentor)
                )
        '''
        for host in query:
            print host.hostname
            for fermentor in host.host_fermentors:
                print fermentor.name, fermentor.start_date, fermentor.start_temp, fermentor.temp_differential
                for probe in fermentor.fermentor_probes:
                    print probe.file_name, probe.type
                fermwrap = fermentor.fermentor_fermwraps.get()
                print fermwrap.pin, fermwrap.in_use
                for schedule in fermentor.fermentor_schedules:
                    print schedule.dt, schedule.temp
        '''
        properties = {}
        try:
            host = query.get()
        except Exception as ex:
            traceback.print_exc(file=sys.stdout)
            raise RuntimeError("DB is screwed up, either missing host, probe or fermwrap: {}".format(ex.message))

        properties['updated'] = host.updated
        properties['hostname'] = host.hostname
        properties['fermentors'] = []
        for fermentor in host.host_fermentors:
            f = {}
            print fermentor.name, fermentor.start_date, fermentor.start_temp, fermentor.temp_differential
            f['id']=fermentor.id
            f['name']=fermentor.name
            f['start_date']=fermentor.start_date.strftime('%Y-%m-%dT%H:%M:%S')
            f['start_temp'] = fermentor.start_temp
            f['temp_differential'] = fermentor.temp_differential
            if fermentor.fermentor_fermwraps.count() > 0:
                fermwrap = fermentor.fermentor_fermwraps.get()
                print fermwrap.pin, fermwrap.in_use
                f['fermwrap_pin'] = fermwrap.pin
            else:
                f['fermwrap_pin'] = None
            f['probes'] = []
            for probe in fermentor.fermentor_probes:
                print probe.file_name, probe.type
                f['probes'].append({'file_name':probe.file_name, 'type':probe.type})
            f['schedule'] = []
            for schedule in fermentor.fermentor_schedules:
                print schedule.dt, schedule.temp
                f['schedule'].append({'dt':schedule.dt.strftime('%Y-%m-%dT%H:%M:%S'), 'temp':schedule.temp})
            properties['fermentors'].append(f)
        properties['fermentors'].sort(key=lambda f:f['name'])

        return properties

    @classmethod
    def read_properties_file(cls):
        properties = open(BREW_PROPERTIES_FILE,'r').readline()
        return properties
    
    @classmethod
    def write_properties_file(cls, properties):
        properties = json.dumps(properties)
        with open(BREW_PROPERTIES_FILE,'w') as f:
            f.write(properties)

    @classmethod
    def blank_properties(cls):
        return {'updated':True,'hostname':socket.gethostname(), 'fermentors':[]}
        

    @classmethod
    def poll_batches(cls, start=False):
        
        '''
        Check local file for updates.

        :param start: The first time the script is executed, bypass checking for updates
        '''
        print ("")
        print ("")
        print ("*************** POLLING ******************")
        print ("")
        print ("")

        updated = False

        if start:
            updated = True

        try:
            properties = cls.read_properties_file() #open(BREW_PROPERTIES_FILE,'r').readlines()
            try:
                properties = json.loads(properties)
            except ValueError as ex:
                traceback.print_exc(file=sys.stdout)
                # json file is invalid json string. Log this and get properties from db
                print "Cannot parse json from {}. Trying DB:".format(BREW_PROPERTIES_FILE),ex.message
                raise IOError("Cannot parse json")
        except IOError as ex:
            traceback.print_exc(file=sys.stdout)
            # This can also be possible if its being run for the first time and the user hasn't added any fermentors?
            print "Cannot read {}. Trying DB:".format(BREW_PROPERTIES_FILE), ex.message, ex.errno
            try:
                properties = cls.read_properties_from_db()
                print "Overwriting {} with that from db.".format(BREW_PROPERTIES_FILE)
                try:
                    cls.write_properties_file(properties)
                    #with open(BREW_PROPERTIES_FILE,'w') as f:
                        #f.write(json.dumps(properties))
                except Exception as ex:
                    traceback.print_exc(file=sys.stdout)
                    print "Cannot write {}!".format(BREW_PROPERTIES_FILE), ex.message

            except peewee.OperationalError as ex:
                traceback.print_exc(file=sys.stdout)
                # Can't connect or query DB. You are screwed!.
                print "cannnot connect to DB for properties: ",ex.message

                # Return in case this is just normal polling with no updates gone bad
                return
            except RuntimeError as ex:
                traceback.print_exc(file=sys.stdout)
                # Nothing returned from DB
                print "Nothing returned from DB!", ex.message
                # Return in case this is just normal polling with no updates gone bad
                return
            except AttributeError as ex:
                traceback.print_exc(file=sys.stdout)
                #DB is wrong!
                print "DB is wrong somehow!", ex.message
                return
            except Exception as ex:
                traceback.print_exc(file=sys.stdout)
                #DB is wrong!
                print "DB is wrong somehow!", ex.message
                return

        if properties['updated']:
            updated = True

        if not updated:
            return

        cls.construct_fermentor_list(properties)

        for fermentor in FermentorList:
            print fermentor
            print "\n"

    @classmethod
    def construct_fermentor_list(cls, properties):
        '''
        properties is a dict of a JSON string in the following form:

            {'updated':True, 'hostname':'raspberrypi',
            'fermentors':[
                {'id':1,
                'name':'Munich Dunkel 100% Munich',
                'start_date':'2015-01-01T00:00:00',
                'start_temp':50.0,
                'temp_differential':0.25,
                'fermwrap_pin':17,
                'probes':[
                    {'file_name':'28-1234567890', 'type':'wort'},
                    {'file_name':'28-0987654321', 'type':'ambient'}
                ]},
                {'id':2,
                'name':'Munich Dunkel 100% Munich',
                'start_date':'2015-01-02T00:00:00',
                'start_temp':50.0,
                'temp_differential':0.25,
                'fermwrap_pin':17,
                'probes':[
                    {'file_name':'28-1234567890', 'type':'wort'},
                    {'file_name':'28-0987654321', 'type':'ambient'}
                ],
                'schedule': [
                    {'dt':'2015-01-03T00:00:00', 'temp':55},
                    {'dt':'2015-01-03T12:00:00', 'temp':60},
                    {'dt':'2015-01-04T00:00:00', 'temp':65}
                    ]
                }
            ]}
        '''
        FermentorList.clear() # This needs to check to see if a fermentor is being removed on the update and turn off its fermwrap

        for fermentor in properties['fermentors']:
            f = Fermentor(name=fermentor['name'],
                          start_temp=fermentor['start_temp'],
                          temp_differential=fermentor['temp_differential'],
                          fermwrap_pin=fermentor['fermwrap_pin'],
                          id=fermentor['id'])

            increases = [ScheduleIncrease(dt=datetime.strptime(i['dt'],'%Y-%m-%dT%H:%M:%S'),temp=i['temp']) for i in fermentor['schedule'] ]

            increases.sort(key=lambda i:i.dt )

            f.schedule = Schedule(start_date=fermentor['start_date'], start_temp=fermentor['start_temp'], increases=increases)

            for probe in fermentor['probes']:
                f.add_probe(Probe(probe_type=probe['type'],file_name=probe['file_name']))


















def start():
    Properties.poll_batches(start=True)

    try:
        while True:
            if len(FermentorList) == 0:
                print("No batches found. Pausing for 30 and then polling.")
                time.sleep(30)
                Properties.poll_batches()

            # Poll for new batches every 30 times
            if Properties.current_poll_count < Properties.POLL_COUNT_MAX:
                Properties.current_poll_count += 1
            else:
                Properties.current_poll_count = 0
                Properties.poll_batches()
                #TODO: What happens if poll_batches fails for some reason? It should retain the original properties in memory and continue noob
                # Actually it looks like the poll will return nothing and so this can continue fine


            try:
                get_db()
            except Exception as ex:
                print "failed to get db", ex.message
                traceback.print_exc(file=sys.stdout)

            dt = datetime.now()
            print dt


            # TODO: Unit test the various probe problems: cannot read, reading 80F, 124F, etc.

            # Get temps
            for fermentor in FermentorList:
                try:
                    fermentor.wort_temp = fermentor.wort_probe.temp # Mandatory
                except IOError as ex:
                    traceback.print_exc(file=sys.stdout)
                    print "Probe is probably disconnected! Cannot read wort temp. Turning off fermwrap.", ex.message
                    fermentor.turn_fermwrap_off()
                    # go to next fermentor so you dont insert previous value
                    continue
                except RuntimeError as ex:
                    traceback.print_exc(file=sys.stdout)
                    print "RuntimeError > 25 second retyring or 185F. Cannot read wort temp. Turning off fermwrap.", ex.message
                    fermentor.turn_fermwrap_off()
                    # go to next fermentor so you dont insert previous value
                    continue
                except Exception as ex:
                    traceback.print_exc(file=sys.stdout)
                    print "Unkown Error. Cannot read wort temp. Turning off fermwrap",ex.message
                    fermentor.turn_fermwrap_off()
                    # go to next fermentor so you dont insert previous value
                    continue


                if hasattr(fermentor, 'ambient_probe'): #Optional
                    try:
                        fermentor.ambient_temp = fermentor.ambient_probe.temp
                    except Exception as ex:
                        #Not a big deal
                        print "Cannot read ambient.", ex.message
                        traceback.print_exc(file=sys.stdout)
                        fermentor.ambient_temp = None
                else:
                    fermentor.ambient_temp = None

                if hasattr(fermentor, 'swamp_probe'): #Optional
                    try:
                        fermentor.swamp_temp = fermentor.swamp_probe.temp
                    except Exception as ex:
                        #Not a big deal
                        print "Cannot read swamp.", ex.message
                        traceback.print_exc(file=sys.stdout)
                        fermentor.swamp_temp = None
                else:
                    fermentor.swamp_temp = None

                # Print to Screen
                print fermentor.name, "range = {} - {}".format(fermentor.min_temp, fermentor.max_temp)
                print '\twort={}'.format(fermentor.wort_temp)
                if hasattr(fermentor, 'ambient_probe'):
                    print '\tambient={}'.format(fermentor.ambient_temp)
                if hasattr(fermentor, 'swamp_probe'):
                    print '\tambient={}'.format(fermentor.swamp_probe)



                # Update Remote MySQL
                # Don't stop program if insert fails
                try:
                    FermentationTemperature.create(fermentor=fermentor.id,
                                               dt=dt,
                                               ambient_temp=fermentor.ambient_temp,
                                               wort_temp=fermentor.wort_temp,
                                               swamp_cooler_temp=fermentor.swamp_temp)
                except Exception as ex:
                    print "Cannot insert into MySQL:", ex.message
                    traceback.print_exc(file=sys.stdout)

                # Check Fermwraps
                #for fermentor in FermentorList:
                if fermentor.wort_temp < fermentor.min_temp:
                    print "\tFermwrap=ON as temp < {}".format(fermentor.min_temp)
                    fermentor.turn_fermwrap_on()

                if fermentor.wort_temp > fermentor.max_temp:
                    print "\tFermwrap=OFF as temp > {}".format(fermentor.max_temp)
                    fermentor.turn_fermwrap_off()

            try:
                get_db().close()
            except Exception as ex:
                print "failed to get db", ex.message
                traceback.print_exc(file=sys.stdout)



            # Sleep
            print "\n"
            time.sleep(5)


    except KeyboardInterrupt:
        print "KeyboardInterrupt. Turning Fermwraps off"
        FermentorList.turn_fermwraps_off()

    except Exception as ex:
        print "Unknown error: ", ex.message
        traceback.print_exc(file=sys.stdout)
        print "Turning Fermwraps off"
        FermentorList.turn_fermwraps_off()