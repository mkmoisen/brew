#!/usr/bin/python
from bottle import Bottle, route, run, template, debug, post, request, static_file
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

@app.route('/fermentor/get')
@app.route('/fermentor/get/')
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
                 'start_date':fermentor.start_date.strftime('%Y-%m-%d %H:%M:%S'),
                 'end_begin_date':fermentor.end_begin_date.strftime('%Y-%m-%d %H:%M:%S'),
                 'end_end_date':fermentor.end_end_date.strftime('%Y-%m-%d %H:%M:%S'),
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
                f['schedules'].append({'dt':schedule.dt.strftime('%Y-%m-%d %H:%M:%S'),
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

def get_hosts():
    get_db()
    hosts = []
    query = (FermentationHost.select())
    for host in query:
        if host not in hosts:
            hosts.append(host)

    return hosts
    get_db().close()



@app.route('/fermentor/')
@app.route('/fermentor')
def fermentor():
    # Get active fermentors
    #fermentors = get_active_fermentors()



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

    

    return template('fermentors', variables)


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
@app.post('/fermentor/add/')
@app.post('/fermentor/add')
def fermentors_add():
    with get_db().transaction:

        fermentor = FermentationFermentor.create(
            name=request.forms.get("name")
            ,start_date=datetime.strptime(request.forms.get("start_date"), '%Y-%m-%d %H:%M:%S')
            ,end_begin_date=datetime.strptime(request.forms.get("end_begin_date"), '%Y-%m-%d %H:%M:%S')
            ,end_end_date=datetime.strptime(request.forms.get("end_end_date"), '%Y-%m-%d %H:%M:%S')
            ,yeast=request.forms.get("yeast")
            ,og=request.forms.get("og")
            ,fg=request.forms.get("og")
            ,start_temp=request.forms.get("start_temp")
            ,temp_differential=request.forms.get("temp_differential")
            ,material=request.forms.get("material")
            ,host=request.forms.get("host_id")
        )

        fermwrap = FermentationFermwrap.get(
            FermentationFermwrap.host==request.forms.get("host_id"),
            FermentationFermwrap.pin==request.forms.get("fermwrap")
        )

        if fermwrap.in_use == 1:
            raise ValueError("Turn the other fermentor using this off noob")

        fermwrap.fermentor = fermentor
        fermwrap.save()

        probe1_file_name = request.forms.get("probe1_file_name")
        probe1_type = request.forms.get("probe1_type")
        probe2_file_name = request.forms.get("probe2_file_name")
        probe2_type = request.forms.get("probe2_type")
        probe3_file_name = request.forms.get("probe3_file_name")
        probe3_type = request.forms.get("probe3_type")

        probes = []
        if probe1_file_name != 'None' and probe1_type != 'None':
            probes.append({'file_name':probe1_file_name, 'type':probe1_type})

        if probe2_file_name != 'None' and probe2_type != 'None':
            probes.append({'file_name':probe2_file_name, 'type':probe2_type})

        if probe3_file_name != 'None' and probe3_type != 'None':
            probes.append({'file_name':probe3_file_name, 'type':probe3_type})

        ambient_count = 0
        wort_count = 0
        swamp_count = 0

        for probe in probes:
            if probe.type == 'ambient':
                ambient_count += 1
            elif probe.type == 'wort':
                wort_count += 1
            elif probe.type == 'swamp':
                swamp_count += 1

        if ambient_count > 1:
            raise ValueError("Too many ambient probes")
        if wort_count > 1:
            raise ValueError("Too many wort probes")
        if wort_count == 0:
            raise ValueError("Need at least one wort probe")
        if swamp_count > 1:
            raise ValueError("too many swamp probes")

        wort_check = FermentationProbe.get(FermentationProbe.file_name==next((probe['file_name'] for probe in probes if probe['type'] == 'wort'), None))
        if wort_check.in_use == 1:
            raise ValueError("Wort probe is already in use noob")

        for probe in probes:
            FermentationProbe.create(file_name=probe['file_name'], type=probe['type'],
                                     host=request.forms.get('host_id'), fermentor=fermentor)


        schedule_indexes = ast.literal_eval(request.forms.get('schedule_index'))

        schedules = []

        for schedule_index in schedule_indexes:
            FermentationSchedule.create(
                fermentor=fermentor
                ,dt=datetime.strptime(request.forms.get('schedule_dt{}'.format(schedule_index)), '%Y-%m-%d %H:%M:%S')
                ,temp=request.forms.get('schedule_temp{}'.format(schedule_index))
            )




    get_db().close()

@app.post('/fermentor/change/')
@app.post('/fermentor/change')
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


    get_db()

    db_fermentor = None

    print "id is ", fermentor['id']

    if fermentor['id'] is None or fermentor['id'] == '':
        print "new lol\n\n\n"
        db_fermentor = FermentationFermentor(
            id = fermentor['id']
            ,name = fermentor['name']
            ,start_date = datetime.strptime(fermentor['start_date'], '%Y-%m-%d %H:%M:%S')
            ,end_begin_date = datetime.strptime(fermentor['end_begin_date'], '%Y-%m-%d %H:%M:%S')
            ,end_end_date = datetime.strptime(fermentor['end_end_date'], '%Y-%m-%d %H:%M:%S')
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
        db_fermentor.start_date = datetime.strptime(fermentor['start_date'], '%Y-%m-%d %H:%M:%S')
        db_fermentor.end_begin_date = datetime.strptime(fermentor['end_begin_date'], '%Y-%m-%d %H:%M:%S')
        db_fermentor.end_end_date = datetime.strptime(fermentor['end_end_date'], '%Y-%m-%d %H:%M:%S')
        db_fermentor.yeast = fermentor['yeast']
        db_fermentor.og = fermentor['og']
        db_fermentor.fg = fermentor['fg']
        db_fermentor.start_temp = fermentor['start_temp']
        db_fermentor.temp_differential = fermentor['temp_differential']
        db_fermentor.material = fermentor['material']
        db_fermentor.host = fermentor['host_id']

    ''' WTF TRANSACTIONS DONT WORK ???? '''

    db_fermentor.save()

    db_fermwrap = FermentationFermwrap.get(FermentationFermwrap.host==db_fermentor.host,
                                           FermentationFermwrap.pin == fermentor['fermwrap'])

    db_fermwrap.fermentor = db_fermentor

    db_fermwrap.save()

    if fermentor['id'] != '' and fermentor['probes_updated']:
        FermentationProbe.delete().where(FermentationProbe.fermentor==db_fermentor)

    if fermentor['id'] == '' or fermentor['probes_updated']:
        db_probes = [FermentationProbe(
            file_name=probe['file_name']
            ,type = probe['type']
            ,fermentor=db_fermentor
            ,host=db_fermentor.host
        ) for probe in fermentor['probes']]

        for db_probe in db_probes:
            print "db_probe fermentor = ", db_probe.fermentor, "id = ", db_probe.fermentor.id
            db_probe.save()

    if fermentor['id'] != '' and fermentor['schedule_updated']:
        FermentationSchedule.select().where(FermentationSchedule.fermentor==db_fermentor).execute()


    if fermentor['id'] == '' or fermentor['schedule_updated']:

        db_schedule = [FermentationSchedule(
            dt=schedule['dt']
            ,temp=schedule['temp']
            ,fermentor=db_fermentor
        ) for schedule in fermentor['schedules']]

        for db_schedule in db_schedule:
            db_schedule.save()



    db_probes = []
    if fermentor['id'] != '':
        FermentationProbe.delete().where(FermentationProbe.fermentor == db_fermentor).execute()


    db_probes = [FermentationProbe(
        file_name=probe['file_name']
        ,type = probe['type']
        ,fermentor=db_fermentor
        ,host=db_fermentor.host
    ) for probe in fermentor['probes']]

    for db_probe in db_probes:
        db_probe.save()


    get_db().close()




