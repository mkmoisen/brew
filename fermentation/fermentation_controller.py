#!/usr/bin/python
from bottle import Bottle, route, run, template, debug, post, request, static_file, response
from datetime import datetime, timedelta
import os
import socket
import ast

from controller import app

from fermentation import FermentationHost, FermentationFermentor, FermentationFermwrap, FermentationProbe, \
    FermentationTemperature, FermentationSchedule

import peewee
from settings import get_db
import json

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


    '''
    query = (FermentationFermentor.select()
                .where(FermentationFermentor.active == 1)
            .join(FermentationHost)
        .switch(FermentationFermentor)
            .join(FermentationProbe, on=FermentationProbe.fermentor)
        .switch(FermentationFermentor)
            .join(FermentationFermwrap, peewee.JOIN_LEFT_OUTER, on=FermentationFermwrap.fermentor)
        .switch(FermentationFermentor).join(FermentationSchedule, peewee.JOIN_LEFT_OUTER, on=FermentationSchedule.fermentor)).aggregate_rows()
    '''

    fermentors = []
    for host in peewee.prefetch(FermentationHost.select(), FermentationFermentor.select(), FermentationProbe.select(), FermentationFermwrap.select(), FermentationSchedule.select()):
        print host.hostname

        for fermentor in host.host_fermentors:
            f = {'id':fermentor.id,
                 'hostname':host.hostname,
                 'host_id':host.id,
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
    default_host_id = FermentationHost.get(FermentationHost.hostname==hostname).id
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

    return template('fermentors')

    # Get active fermentors
    #fermentors = get_active_fermentors()


    '''
    # Get hosts
    hosts = get_hosts()

    hostname = socket.gethostname()

    fermwraps = [17,18,22,23,24,25] # Can I get these from the DB?

    # Get dates
    today = datetime.now()
    four_weeks_later = today + timedelta(days=28)
    six_weeks_later = today + timedelta(days=42)
    today = datetime.strftime(today, '%Y-%m-%d %H:%M:%S')
    four_weeks_later = datetime.strftime(four_weeks_later, '%Y-%m-%d %H:%M:%S')
    six_weeks_later = datetime.strftime(six_weeks_later, '%Y-%m-%d %H:%M:%S')

    # Get temperature Probes
    process = os.popen('ls /sys/bus/w1/devices/ | grep 28')
    preprocessed = process.read()
    process.close()
    probes = preprocessed.split('\n')[:-1]
    probes.insert(0, 'None')

    probe_types = ['None','ambient','wort','swamp'] # Can I get these from peewee model instead?


    variables = {#'fermentors':fermentors,
                 'hosts':hosts,
                 'probe_types':probe_types,
                 'probes':probes,
                 'fermwraps':fermwraps,
                 'today':today,
                 'four_weeks_later':four_weeks_later,
                 'six_weeks_later':six_weeks_later,
                 'hostname':hostname}

    get_db().close()
    '''
    

    #return template('fermentors', variables)



'''

        $scope.fermentors = [
            % for fermentor in fermentors:
                % index_order[fermentor.id] = index
                % index += 1
                {
                    id:{{fermentor.id}},
                    hostname:'{{fermentor.host.hostname}}',
                    host_id:{{fermentor.host.id}},
                    name:'{{fermentor.name}}',
                    % for fermwrap in fermentor.fermentor_fermwraps:
                    fermwrap:{{fermwrap.pin}},
                    % end
                    start_date:'{{fermentor.start_date}}',
                    end_begin_date:'{{fermentor.end_begin_date}}',
                    end_end_date:'{{fermentor.end_end_date}}',
                    start_temp:{{fermentor.start_temp}},
                    temp_differential:{{fermentor.temp_differential}},
                    yeast:'{{fermentor.yeast}}',
                    og:{{fermentor.og}},
                    fg:{{!'null' if fermentor.fg is None else fermentor.fg}},
                    material:'{{fermentor.material}}',
                    probes:[
                        % for probe in fermentor.fermentor_probes:
                            {
                                file_name:'{{probe.file_name}}',
                                type:'{{probe.type}}'
                            },
                        % end
                    ],schedules:[
                        % schedule_index = 0
                        % for schedule in fermentor.fermentor_schedules:
                            {
                                dt:'{{schedule.dt}}',
                                temp:{{schedule.temp}},
                                index:{{schedule_index}}
                            },
                            % schedule_index += 1
                        % end
                    ],
                },
            % end
        ];
'''


@app.post('/fermentation/fermentor/change/')
@app.post('/fermentation/fermentor/change')
def fermentors_change():

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


    with get_db().atomic():
        db_fermentor = None

        print "id is ", fermentor['id']

        if fermentor['id'] is None:
            print "new lol\n\n\n"
            db_fermentor = FermentationFermentor(
                id = fermentor['id']
                ,name = fermentor['name']
                ,start_date = datetime.strptime(fermentor['start_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
                ,end_begin_date = datetime.strptime(fermentor['end_begin_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
                ,end_end_date = datetime.strptime(fermentor['end_end_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
                ,yeast = fermentor['yeast']
                ,og = fermentor['og']
                ,fg = fermentor['fg']
                ,start_temp = fermentor['start_temp']
                ,temp_differential = fermentor['temp_differential']
                ,material = fermentor['material']
                ,host = fermentor['host_id']
            )
        else :
            db_fermentor = FermentationFermentor.get(id=fermentor['id'])
            db_fermentor.name = fermentor['name']
            db_fermentor.start_date = datetime.strptime(fermentor['start_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
            db_fermentor.end_begin_date = datetime.strptime(fermentor['end_begin_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
            db_fermentor.end_end_date = datetime.strptime(fermentor['end_end_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
            db_fermentor.yeast = fermentor['yeast']
            db_fermentor.og = fermentor['og']
            db_fermentor.fg = fermentor['fg']
            db_fermentor.start_temp = fermentor['start_temp']
            db_fermentor.temp_differential = fermentor['temp_differential']
            db_fermentor.material = fermentor['material']
            db_fermentor.host = fermentor['host_id']

        ''' WTF TRANSACTIONS DONT WORK ???? '''

        db_fermentor.save()




        if fermentor['fermwrap_updated']:

            db_new_fermwrap = FermentationFermwrap.get(FermentationFermwrap.host==db_fermentor.host,
                                               FermentationFermwrap.pin == fermentor['fermwrap'])

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


        if fermentor['id'] is not None and fermentor['probes_updated']:
            FermentationProbe.delete().where(FermentationProbe.fermentor==db_fermentor)

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

        if fermentor['id'] is not None and fermentor['schedule_updated']:
            FermentationSchedule.select().where(FermentationSchedule.fermentor==db_fermentor).execute()


        if fermentor['id'] is None or fermentor['schedule_updated']:

            db_schedule = [FermentationSchedule(
                dt=schedule['dt']
                ,temp=schedule['temp']
                ,fermentor=db_fermentor
            ) for schedule in fermentor['schedules']]

            for db_schedule in db_schedule:
                db_schedule.save()



        db_probes = []
        if fermentor['id'] is not None:
            FermentationProbe.delete().where(FermentationProbe.fermentor == db_fermentor).execute()


        db_probes = [FermentationProbe(
            file_name=probe['file_name']
            ,type = probe['type']
            ,fermentor=db_fermentor
            ,host=db_fermentor.host
        ) for probe in fermentor['probes']]

        for db_probe in db_probes:
            db_probe.save()

        #raise Exception("LOL")

    get_db().close()

    # This should return some 200 message probably.
    #if fermentor['id'] == '':
    response.status = 201




