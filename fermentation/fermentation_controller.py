#!/usr/bin/python
from bottle import Bottle, route, run, template, debug, post, request, static_file, response
from datetime import datetime, timedelta
import os
import socket
import ast

from controller import app

from fermentation import FermentationHost, FermentationFermentor, FermentationFermwrap, FermentationProbe, \
    FermentationTemperature, FermentationSchedule, FermentationFermwrapHistory, Properties

import peewee
from settings import get_db
import json

import errno

if __name__ == '__main__':
    print "fermentation main lol"

'''
query = (FermentationFermentor.select()
        .where(FermentationFermentor.active == 1)
    .join(FermentationHost)
.switch(FermentationFermentor)
    .join(FermentationProbe, on=FermentationProbe.fermentor)
.switch(FermentationFermentor)
    .join(FermentationFermwrap, peewee.JOIN_LEFT_OUTER, on=FermentationFermwrap.fermentor)
.switch(FermentationFermentor)
    .join(FermentationSchedule, peewee.JOIN_LEFT_OUTER, on=FermentationSchedule.fermentor)
)

query = peewee.prefetch(FermentationHost.select(), FermentationFermentor)
for host in query:
    print host.hostname
    for fermentor in host.host_fermentors_prefetch:
        print fermentor.name
'''


'''
This should probably be changed to /fermentation/fermentor/get
'''
@app.route('/fermentation/fermentor/get')
@app.route('/fermentation/fermentor/get/')
def get_active_fermentors():
    print "IS IT CLOSED YO ?", get_db().is_closed()
    get_db()

    fermentors = []

    query = (FermentationFermentor.select(FermentationFermentor, FermentationHost, FermentationProbe, FermentationFermwrap, FermentationSchedule)
                .where(FermentationFermentor.active == 1)
            .join(FermentationHost)
        .switch(FermentationFermentor)
            .join(FermentationProbe, on=FermentationProbe.fermentor)
        .switch(FermentationFermentor)
            .join(FermentationFermwrap, peewee.JOIN_LEFT_OUTER, on=FermentationFermwrap.fermentor)
        .switch(FermentationFermentor)
             .join(FermentationSchedule, peewee.JOIN_LEFT_OUTER, on=FermentationSchedule.fermentor)
        .aggregate_rows()
    )

    '''
    q_hosts = FermentationHost.select()
    q_fermentors = FermentationFermentor.select().where(FermentationFermentor.name=='obama', FermentationFermentor.active==1)
    q_probes = FermentationProbe.select().where(FermentationProbe.in_use==1)
    q_fermwrap = FermentationFermwrap.select().where(FermentationFermwrap.in_use==1)
    q_schedule = FermentationSchedule.select()

    query = peewee.prefetch(q_hosts, q_fermentors, q_probes, q_fermwrap, q_schedule)
    print dir(query)
    print "where = ", query.where
    print "query = ", query

    '''
    '''
    for host in peewee.prefetch(FermentationHost.select(),
                                FermentationFermentor.select().where(FermentationFermentor.active==1),
                                FermentationProbe.select().where(FermentationProbe.in_use==1),
                                FermentationFermwrap.select().where(FermentationFermwrap.in_use==1),
                                FermentationSchedule.select()):
    '''
    #for host in query:
        #print host.hostname
    for fermentor in query:
    #    for fermentor in host.host_fermentors:
            f = {'id':fermentor.id,
                 #'hostname':host.hostname,
                 #'host_id':host.id,
                 'hostname':fermentor.host.hostname,
                 'host_id':fermentor.host.id,
                 'name':fermentor.name,
                 'start_date':fermentor.start_date.strftime('%Y-%m-%dT%H:%M:%S'),
                 'end_begin_date':fermentor.end_begin_date.strftime('%Y-%m-%dT%H:%M:%S'),
                 'end_end_date':fermentor.end_end_date.strftime('%Y-%m-%dT%H:%M:%S'),
                 'start_temp':fermentor.start_temp,
                 'temp_differential':fermentor.temp_differential,
                 'yeast':fermentor.yeast,
                 'og':fermentor.og,
                 'fg':fermentor.fg,
                 'material':fermentor.material,
                 }

            fermentors.append(f)


            for fermwrap in fermentor.fermentor_fermwraps:
                f['fermwrap']=fermwrap.pin

            f['probes'] = []
            for probe in fermentor.fermentor_probes:
                f['probes'].append({'file_name':probe.file_name,
                                   'type':probe.type})
            f['schedules'] = []
            for schedule in fermentor.fermentor_schedules:
                f['schedules'].append({'dt':schedule.dt.strftime('%Y-%m-%dT%H:%M:%S'),
                                      'temp':schedule.temp})

    for fermentor in fermentors:
        print "\t",fermentor['name']
        for probe in fermentor['probes']:
            print "\t",probe['file_name']
        if 'fermwrap' in fermentor:
            print "\t",fermentor['fermwrap']
        for schedule in fermentor['schedules']:
            print "\t",schedule['dt'], schedule['temp']
    '''
    for fermentor in query:
        if fermentor not in fermentors:
            fermentors.append(fermentor)

    print "fermentors len = ",len(fermentors)

    for fermentor in fermentors:
        print fermentor.host.hostname, fermentor.name, fermentor.start_date, fermentor.end_begin_date, \
            fermentor.end_end_date, fermentor.yeast, fermentor.og, fermentor.fg, fermentor.start_temp, \
            fermentor.temp_differential, fermentor.active, fermentor.material
        for probe in fermentor.fermentor_probes:
            print "\t", probe.file_name, probe.type
        for fermwrap in fermentor.fermentor_fermwraps:
            print fermwrap.pin
        for schedule in fermentor.fermentor_schedules:
            print schedule.dt, schedule.temp

    get_db().close()
    '''

    return json.dumps(fermentors)

'''
This should probably be changed to /fermentation/host/get
'''
@app.route('/fermentation/host/get')
@app.route('/fermentation/host/get/')
def get_hosts():
    print "get_hosts()"
    get_db()
    hosts = []
    query = (FermentationHost.select())

    for host in query:
        hosts.append({'id':host.id,
                      'hostname':host.hostname})

    get_db().close()

    for host in hosts:
        print host

    return json.dumps(hosts)
    

'''
This should probably be changed to /fermentation/fermwraps/get
'''
@app.route('/fermentation/fermwrap/get')
@app.route('/fermentation/fermwrap/get/')
def get_fermwraps():
    print "get_fermwraps()"
    get_db()

    # Is it possible that two hosts have differening number of pins if they are using two different models of RPi?
    query = (FermentationFermwrap.select(FermentationFermwrap.pin).distinct())
    fermwraps = []
    for fermwrap in query:
        fermwraps.append({'fermwrap':fermwrap.pin})

    get_db().close()

    for fermwrap in fermwraps:
        print fermwrap
    return json.dumps(fermwraps)

@app.route('/fermentation/fermwrap/get/host-id/<host_id>')
@app.route('/fermentation/fermwrap/get/host-id/<host_id>/')
def get_available_fermwraps(host_id):
    get_db()

    query = (FermentationFermwrap.select(FermentationFermwrap.pin)
                .where(FermentationFermwrap.host==int(host_id),
                         FermentationFermwrap.in_use == 0)
    )
    fermwraps = []
    for fermwrap in query:
        fermwraps.append({'fermwrap':fermwrap.pin})

    get_db().close()
    for fermwrap in fermwraps:
        print fermwrap

    return json.dumps(fermwraps)

'''
This should probably be changed to /fermentation/host/get
'''
@app.route('/fermentation/default/get')
@app.route('/fermentation/default/get/')
def get_default_values():
    print "get_default_values()"

    hostname = socket.gethostname()
    try:
        default_host_id = FermentationHost.get(FermentationHost.hostname==hostname).id
    except peewee.DoesNotExist:
        default_host_id = None

    default_temp = 65
    default_temp_differential = 0.125
    default_material = 'glass'

    default_today = datetime.now()
    default_end_begin_date = default_today + timedelta(days=28)
    default_end_end_date = default_today + timedelta(days=42)
    default_today = default_today.strftime('%Y-%m-%dT%H:%M:%S')
    default_end_begin_date = default_end_begin_date.strftime('%Y-%m-%dT%H:%M:%S')
    default_end_end_date = default_end_end_date.strftime('%Y-%m-%dT%H:%M:%S')

    ret = {
        'default_today':default_today,
        'default_end_begin_date':default_end_begin_date,
        'default_end_end_date':default_end_end_date,
        'default_host_id':default_host_id,
        'default_temp':default_temp,
        'default_temp_differential':default_temp_differential,
        'default_material':default_material,
    }

    for d in ret:
        print d

    return json.dumps(ret)

@app.route('/fermentation/probe_type/get')
@app.route('/fermentation/probe_type/get/')
def get_probe_types():
    print "get_probe_types()"
    # this should be retrieved dynamically
    return json.dumps(['wort','ambient', 'swamp'])

@app.route('/fermentation/probe/get')
@app.route('/fermentation/probe/get/')
def get_probes():
    print "get_probes()"
    # Get temperature Probes
    process = os.popen('ls /sys/bus/w1/devices/ | grep 28')
    preprocessed = process.read()
    process.close()
    probes = preprocessed.split('\n')[:-1]
    # This should throw some error or warning if no probes are available in the RPi

    if not probes:
        probes = ['28-1234567890','28-0987654321', '28-obama','28-yomama']

    # What happens if the end user used the wrong RPi's website? You won't show him the correct hosts.
    return json.dumps(probes)



@app.route('/fermentation/')
@app.route('/fermentation')
def fermentor():
    #return static_file('fermentors.tpl', 'views/')
    return template('fermentors')




@app.route('/fermentation/temperature/raw/get')
@app.route('/fermentation/temperature/raw/get/')
def get_raw_temperature():
    get_db()

    query = (FermentationTemperature.select(FermentationTemperature, FermentationFermentor)
           .join(FermentationFermentor, on=FermentationTemperature.fermentor)
                .where(FermentationFermentor.active == 1)
           .order_by(FermentationTemperature.dt.desc())
           .limit(100)
    )
    temps = []
    for temp in query:
        temps.append({
            'hostname':temp.fermentor.host.hostname,
            'fermentor':temp.fermentor.name,
            'dt':temp.dt.strftime('%Y-%m-%dT%H:%M:%S'),
            'ambient_temp':temp.ambient_temp,
            'wort_temp':temp.wort_temp,
            'target_temp':temp.target_temp,
            'is_fermwrap_on':temp.is_fermwrap_on,
            'fermwrap_turned_on_now':temp.fermwrap_turned_on_now,
            'fermwrap_turned_off_now':temp.fermwrap_turned_off_now,

        })

    get_db().close()

    return json.dumps(temps)

@app.route('/fermentation/fermwrap-history/get')
@app.route('/fermentation/fermwrap-history/get/')
def get_fermwrap_history():
    get_db()

    query = (
        FermentationFermwrapHistory.select()
        .join(FermentationFermentor, on=FermentationFermwrapHistory.fermentor)
            .where(FermentationFermentor.active==1)
        .order_by(FermentationFermwrapHistory.dt.desc())
        .limit(100)
    )

    fermwraps = []

    for fermwrap in query:
        fermwraps.append({
            'fermentor':fermwrap.fermentor.name,
            'dt':fermwrap.dt.strftime('%Y-%m-%dT%H:%M:%S'),
            'ambient_temp':fermwrap.ambient_temp,
            'target_temp_at_start':fermwrap.target_temp_at_start,
            'target_temp_at_end':fermwrap.target_temp_at_end,
            'temp_differential':fermwrap.temp_differential,
            'minutes_heater_on':fermwrap.minutes_heater_on,
            'minutes_heater_off':fermwrap.minutes_heater_off,
        })

    get_db().close()

    return json.dumps(fermwraps)

@app.route('/fermentation/fermwrap-history/get/csv')
@app.route('/fermentation/fermwrap-history/get/csv/')
def get_fermwrap_history_csv():
    get_db()

    query = (
        FermentationFermwrapHistory.select()
        .join(FermentationFermentor, on=FermentationFermwrapHistory.fermentor)
            .where(FermentationFermentor.active==1)
        .order_by(FermentationFermwrapHistory.dt.desc())
        .aggregate_rows()
    )


    fermwraps = ['fermentor,dt,ambient_temp,target_temp_at_start,target_temp_at_end,temp_differential,minutes_heater_on,minutes_heater_off\n']

    for fermwrap in query:
        fermwraps.append(','.join(map(str,[fermwrap.fermentor.name,fermwrap.dt.strftime('%Y-%m-%dT%H:%M:%S'),fermwrap.ambient_temp,
                                   fermwrap.target_temp_at_start,fermwrap.target_temp_at_end,fermwrap.temp_differential,
                                   fermwrap.minutes_heater_on,fermwrap.minutes_heater_off,])) + '\n')

    get_db().close()

    return json.dumps(fermwraps)

@app.route('/fermentation/history/csv')
@app.route('/fermentation/history/csv')
def fermentor_history():
    return template('fermentor_history_csv')

@app.route('/fermentation/history')
@app.route('/fermentation/history/')
def fermentor_history():
    return template('fermentor_history')


@app.post('/fermentation/fermentor/inactivate')
@app.post('/fermentation/fermentor/inactivate/')
def fermentor_inactivate():
    fermentor = json.loads(request.forms.dict.keys()[0])
    print "fermentor = ", fermentor

    # Prepare to edit properties file # need to change this to account for multiple RPis
    should_write_properties = True
    try:
        properties = Properties.read_properties_file()
        try:
            properties = json.loads(properties)
        except ValueError as ex:
            pass
            # Why would this happen?
            print "COULDNT READ JSON ", ex.message
            should_write_properties = False
        except Exception as ex:
            pass
            # Why would this happen?
            print "COULDNT READ JSON ", ex.message
            should_write_properties = False
    except IOError as ex:
        print "COULDNT READ FILE ", ex.message, ex.errno

        if ex.errno == errno.ENOENT:
            # Cannot find file on disk. Assume this means this is the first time for the user
            properties = Properties.blank_properties()
        else:
            # Maybe Read only file system or something else. Probably cannot write properties file anyways.
            # Would it be safer to not even try writing this modified blank properties file? What if i couldn't read
            # right now but by the end of this method could write? That would be bad!
            properties = Properties.blank_properties()
            should_write_properties = False

    properties['updated']=True
    properties['fermentors'][:] = [item for item in properties['fermentors'] if item['id'] != fermentor['id']]
    with get_db().atomic():
        print "inactivating fermwrap"
        is_fermwrap = False
        try:
            fermwrap = FermentationFermwrap.get(FermentationFermwrap.fermentor==fermentor['id'])
            is_fermwrap = True
        except FermentationFermwrap.DoesNotExist:
            pass

        if is_fermwrap:
            fermwrap.fermentor = None
            fermwrap.in_use = 0
            fermwrap.save()

        print "inactivating probe"
        for probe in FermentationProbe.select().where(FermentationProbe.fermentor==fermentor['id']):
            probe.in_use = 0
            probe.save()

        print "inactivating fermwrap"
        fermentor = FermentationFermentor.get(FermentationFermentor.id==fermentor['id'])
        fermentor.active = 0
        fermentor.save()

    get_db().close()

    if should_write_properties:
        Properties.write_properties_file(properties)





@app.post('/fermentation/fermentor/change/')
@app.post('/fermentation/fermentor/change')
def fermentors_change():
    '''
    One tricky thing here is how to update the brew.properties file on disk.
    Do I pull the outdated properties from file into memory, and operate on them independently
    of the database transaction?

    The goal is to never be dependent on the stupid remote godaddy mysql db again.

    I also need to edit the brew.properties on ALL the RPis, or force the user to only edit the RPi on each host individually

    :return:
    '''

    '''
    print "hai"
    print "fermentor = "
    print request.forms.get('fermentor')
    print "wtf request.forms == {}".format(request.forms)
    print "dir = {}".format(dir(request.forms))
    print "dict = {}".format(request.forms.dict)
    print "for key lol"
    for key in request.forms:
        print "string\n"
        print key
        print "\n\njson"
        print json.loads(key)
    '''
    fermentor = json.loads(request.forms.dict.keys()[0])
    print "\n\nsuper lol"
    print fermentor

    data = {}

    # Prepare to edit properties file # need to change this to account for multiple RPis
    should_write_properties = True
    try:
        properties = Properties.read_properties_file()
        try:
            properties = json.loads(properties)
        except ValueError as ex:
            pass
            # Why would this happen?
            print "COULDNT READ JSON ", ex.message
            should_write_properties = False
        except Exception as ex:
            pass
            # Why would this happen?
            print "COULDNT READ JSON ", ex.message
            should_write_properties = False
    except IOError as ex:
        print "COULDNT READ FILE ", ex.message, ex.errno

        if ex.errno == errno.ENOENT:
            # Cannot find file on disk. Assume this means this is the first time for the user
            properties = Properties.blank_properties()
        else:
            # Maybe Read only file system or something else. Probably cannot write properties file anyways.
            # Would it be safer to not even try writing this modified blank properties file? What if i couldn't read
            # right now but by the end of this method could write? That would be bad!
            properties = Properties.blank_properties()
            should_write_properties = False



    properties['updated']=True

    with get_db().atomic():
        db_fermentor = None

        print "id is ", fermentor['id']

        properties_fermentor = {}

        if fermentor['id'] is None:
            # Initialize the brew.properteis fermentor for new fermentor

            db_fermentor = FermentationFermentor(
                id = fermentor['id']
                ,name = fermentor['name']
                ,start_date = datetime.strptime(fermentor['start_date'], '%Y-%m-%dT%H:%M:%S')
                ,end_begin_date = datetime.strptime(fermentor['end_begin_date'], '%Y-%m-%dT%H:%M:%S')
                ,end_end_date = datetime.strptime(fermentor['end_end_date'], '%Y-%m-%dT%H:%M:%S')
                ,yeast = fermentor['yeast']
                ,og = fermentor['og']
                ,fg = fermentor['fg']
                ,start_temp = fermentor['start_temp']
                ,temp_differential = fermentor['temp_differential']
                ,material = fermentor['material']
                ,host = fermentor['host_id']
            )

            # Take care of fermwrap pin below
        else :
            # Get fermentor from brew.properteis on disk if this is an update
            properties_fermentor = next((item for item in properties['fermentors'] if item['id'] == fermentor['id']), None)

            if properties_fermentor is None:
                #TODO: This is a big mistake if this line gets triggered. Either I'm trying to update the wrong RPi or something catastrophic happened
                raise Exception("NOOB")
            db_fermentor = FermentationFermentor.get(id=fermentor['id'])
            db_fermentor.name = fermentor['name']
            db_fermentor.start_date = datetime.strptime(fermentor['start_date'], '%Y-%m-%dT%H:%M:%S')
            db_fermentor.end_begin_date = datetime.strptime(fermentor['end_begin_date'], '%Y-%m-%dT%H:%M:%S')
            db_fermentor.end_end_date = datetime.strptime(fermentor['end_end_date'], '%Y-%m-%dT%H:%M:%S')
            db_fermentor.yeast = fermentor['yeast']
            db_fermentor.og = fermentor['og']
            db_fermentor.fg = fermentor['fg']
            db_fermentor.start_temp = fermentor['start_temp']
            db_fermentor.temp_differential = fermentor['temp_differential']
            db_fermentor.material = fermentor['material']
            db_fermentor.host = fermentor['host_id']


        db_fermentor.save()

        if fermentor['id'] is None:
            properties_fermentor['id'] = db_fermentor.id
            properties_fermentor['probes'] = []
            properties_fermentor['schedule'] = []

        #create/modify brew.properties fermentor
        properties_fermentor['name'] = db_fermentor.name
        properties_fermentor['start_date'] = db_fermentor.start_date.strftime('%Y-%m-%dT%H:%M:%S')
        properties_fermentor['start_temp'] = db_fermentor.start_temp
        properties_fermentor['temp_differential'] = db_fermentor.temp_differential




        ## FERMWRAP ##
        if fermentor['fermwrap_updated']:

            db_new_fermwrap = FermentationFermwrap.get(FermentationFermwrap.host==db_fermentor.host,
                                               FermentationFermwrap.pin == fermentor['fermwrap'])

            # Set the brew.properties fermwrap
            properties_fermentor['fermwrap_pin'] = int(fermentor['fermwrap'])

            if fermentor['id'] is None:
                if db_new_fermwrap.in_use == 1:
                    raise Exception("Fermwrap in use by another fermentor: ", db_new_fermwrap.fermentor.name)
            else:
                db_old_fermwrap = FermentationFermwrap.get(FermentationFermwrap.fermentor==db_fermentor)
                db_old_fermwrap.fermentor = None
                db_old_fermwrap.in_use = 0
                db_old_fermwrap.save()

            db_new_fermwrap.fermentor = db_fermentor
            db_new_fermwrap.in_use = 1
            db_new_fermwrap.save()

        else:
            # Set the brew.properties fermwrap
            if fermentor['id'] is None:
                properties_fermentor['fermwrap_pin'] = None # User isn't using fermwrap for some reason



        ### PROBES ###
        if fermentor['id'] is not None and fermentor['probes_updated']:
            FermentationProbe.delete().where(FermentationProbe.fermentor==db_fermentor).execute()
            #unset for editing brew.properties fermentor
            properties_fermentor['probes']=[]

        if fermentor['id'] is None or fermentor['probes_updated']:
            db_probes = [FermentationProbe(
                file_name=probe['file_name']
                ,type = probe['type']
                ,fermentor=db_fermentor
                ,host=db_fermentor.host
            ) for probe in fermentor['probes']]

            for db_probe in db_probes:
                print "db_probe fermentor = ", db_probe.fermentor, "id = ", db_probe.fermentor.id
                db_probe.save()

            properties_fermentor['probes'] = [{'file_name':p['file_name'], 'type':p['type']} for p in fermentor['probes']]



        ### SCHEDULE ###
        if fermentor['id'] is not None and fermentor['schedule_updated']:
            FermentationSchedule.delete().where(FermentationSchedule.fermentor==db_fermentor).execute()
            # Unset for brew.properties fermentor
            properties_fermentor['schedule'] = []

        if fermentor['id'] is None or fermentor['schedule_updated']:

            db_schedule = [FermentationSchedule(
                dt=schedule['dt'] # ?? How is this parsing to the correct date? Is this Peewee?
                ,temp=schedule['temp']
                ,fermentor=db_fermentor
            ) for schedule in fermentor['schedules']]

            for db_schedule in db_schedule:
                db_schedule.save()

            properties_fermentor['schedule'] = [{'dt':s['dt'], 'temp':float(s['temp'])} for s in fermentor['schedules']]



        if fermentor['id'] is None:
            response.status = 201
            data['fermentor_id']=db_fermentor.id
        else:
            response.status = 200

        # Put brew.properties fermentor back in file
        if fermentor['id'] is None:
            properties['fermentors'].append(properties_fermentor)
        # for edited fermentors, arrays should have a reference pointer to the dict I just edited. It should be good to save now.

        ### OK what if it fails to write here?
        # If the file system is read only, that is fine because poll will pick it up from DB.
        # But if its just a temporary write problem, then poll will read from outdated file system!
        if should_write_properties:
            Properties.write_properties_file(properties)


    get_db().close()




    return json.dumps(data)


    # This should return some 200 message probably.
    #if fermentor['id'] == '':




test = [{'id':1,'name':'matt'}, {'id':2,'name':'mark'}]

lol = next((item for item in test if item['name'] == 'matt'), None)

lol['name']='LOLOL'
lol
test