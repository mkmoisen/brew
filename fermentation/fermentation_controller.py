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


def get_active_fermentors():
    print "IS IT CLOSED YO ?", get_db().is_closed()
    get_db()



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

    fermentors = []

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

    return fermentors

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
    fermentors = get_active_fermentors()

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


    variables = {'fermentors':fermentors,
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
    get_db()

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

    fermentor = json.loads(request.forms.dict.keys()[0])
    print "\n\nsuper lol"
    print fermentor

    return

    db_fermentor = FermentationFermentor(
        id = fermentor['id']
        ,name = fermentor['name']
        ,start_date = datetime.strptime(fermentor['start_date'], '%Y-%m-%d %H:%M%:S')
        ,end_begin_date = datetime.strptime(fermentor['end_begin_date'], '%Y-%m-%d %H:%M%:S')
        ,end_end_date = datetime.strptime(fermentor['end_end_date'], '%Y-%m-%d %H:%M%:S')
        ,yeast = fermentor['yeast']
        ,og = fermentor['og']
        ,fg = fermentor['fg']
        ,start_temp = fermentor['start_temp']
        ,temp_differential = fermentor['temp_differential']
        ,active = fermentor['active']
        ,material = fermentor['material']
        ,host = fermentor['host_id']
    )

    # For edits
    db_fermwrap = FermentationFermwrap.select().where(
        # Should I check to see if that pin is already in use?
        fermentor=db_fermentor.id
    )
    if db_fermwrap.pin != fermentor['fermwrap']:
        db_fermwrap.pin = fermentor['fermwrap']
        db_fermwrap.update()

    db_probes = []
    if db_fermentor.id is not None:
        # Shouldn't I actually check for updates first before deleting unecessarily?
        for db_probe in FermentationProbe.select().where(
            FermentationProbe.fermentor == db_fermentor
        ):
            db_probe.delete()


    db_probes = [FermentationProbe(
        file_name=probe['file_name']
        ,type = probe['type']
        ,fermentor=db_fermentor
        ,host=db_fermentor.host.id
    ) for probe in fermentor['probes']]

    for db_probe in db_probes:
        db_probe.save()






    get_db().close()




