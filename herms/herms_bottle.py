#!/usr/bin/python
'''
import ast
import threading
import json

from bottle import Bottle, run, template, debug, request, static_file

from herms.herms import *

app = Bottle()

herms = None

@app.route('/setup')
def setup():
    #Search file system for DS18B20s
    process = os.open('ls /sys/bus/w1/devices/ | grep 28')
    preprocessed = process.read()
    process.close()

    probes = preprocessed.split('\n')[:-1]

    #probes = ['28-123456789', '28-987654321']

    #Available pins on RPi for PowerTail Switch 2
    pins = [17,18,22,23,24,25]

    variables = {'probes': probes,
                 'pins' : pins}

    return template('herms_setup', variables)


def herms_get_variables():
    hlt_temp = herms.hlt_temp
    mashtun_temp = herms.mashtun_temp
    total_duration = herms.time_elapsed
    steps = herms.steps
    current_step_index = herms.current_step_index
    current_step = herms.current_step
    current_step_duration = herms.current_step.time_elapsed
    is_heating_on = herms.heating.is_on
    pump = herms.pump
    is_pump_on = herms.pump.is_on
    initialized_strike_water = herms.initialized_strike_water
    strike_completed = herms.strike_completed
    strike_water_temp = herms.strike_water_temp
    herms_complete = herms.herms_complete
    strike_duration = herms.strike_time_elapsed()
    strike_data = herms.strike_data
    data = json.dumps(herms.data)

    variables = {'hlt_temp':hlt_temp,
                 'mashtun_temp':mashtun_temp,
                 'total_duration':total_duration,
                 'steps':steps,
                 'current_step_index':current_step_index,
                 'current_step':current_step,
                 'current_step_duration':current_step_duration,
                 'is_heating_on':is_heating_on,
                 'pump':pump,
                 'is_pump_on':is_pump_on,
                 'initialized_strike_water':initialized_strike_water,
                 'strike_completed':strike_completed,
                 'strike_water_temp':strike_water_temp,
                 'herms_complete':herms_complete,
                 'data':data,
                 'strike_duration':strike_duration,
                 'strike_data':strike_data}

    return variables

@app.route('/brew')
def herms_get():
    # Redirect to Setup if it hasn't been initialized
    if herms is None:
        return setup()

    variables = herms_get_variables()

    return template('brew', variables)


@app.post('/brew')
def herms_init():
    global herms

    room_temp = float(request.forms.get('room_temp'))
    water_grist_ratio = float(request.forms.get('water_grist_ratio'))

    hlt_probe_file_name = request.forms.get('hlt_probe_file_name')
    mashtun_probe_file_name = request.forms.get('mashtun_probe_file_name')

    pins = request.forms.getall('selected_pins')
    pump_pin = int(request.forms.get('selected_pump_pin'))

    step_indexes = ast.literal_eval(request.forms.get('step_index'))


    hlt_probe = Probe(probe_name="hlt", file_name=hlt_probe_file_name)
    print hlt_probe
    mashtun_probe = Probe(probe_name="mashtun", file_name=mashtun_probe_file_name)
    print mashtun_probe

    heating = Heating(heaters = [Heater(int(pin)) for pin in pins])

    pump = Pump(pin=pump_pin)
    print heating

    steps = []
    for step_index in step_indexes:
        steps.append(Step(name=request.forms.get('step_name{}'.format(step_index)),
                          duration=request.forms.get('step_duration{}'.format(step_index)),
                          temp=request.forms.get('step_temp{}'.format(step_index))
                          ))
    print steps
    herms = Herms(hlt_probe=hlt_probe,
                  mashtun_probe=mashtun_probe,
                  heating=heating,
                  pump=pump,
                  steps=steps,
                  room_temp=room_temp,
                  water_grist_ratio=water_grist_ratio)

    # Start heating up Strike Water
    t = threading.Thread(target=herms.initialize_strike_water)
    t.start()

    return herms_get()

@app.route('/herms_ajax')
def test_chart():
    data = herms.data

    ret = json.dumps(data)

    return ret

@app.post('/strike_ready')
def strike_ready():
    # If temp has fallen down by the time the user clicked submit
    if not herms.initialized_strike_water:
        return herms_get()

    # User is ready to strike. Stop pump and kill thread on brew.initialize_strike_water()
    herms.strike_ready = True

    return herms_get()

@app.post('/strike_complete')
def strike_complete():
    # User has striked.


    herms.strike_completed = True

    # Starts first Step
    t = threading.Thread(target=herms.run)
    t.start()

    return herms_get()


a = 1
@app.route('/test_chart')
def test_chart():
    global a
    data = [[a, a, a + 10] for a in range(1, a + 1)]

    ret = json.dumps(data)
    variables = {'data':ret}

    return template('test_chart', variables)


@app.route('/test_chart_ajax')
def test_chart():
    global a
    a += 1
    data = [[a, a**2, a + 10] for a in range(1, a + 1)]

    ret = json.dumps(data)

    return ret


debug(True)
#run(app, server="meinheld", host='0.0.0.0', port='8080', reloader=True)
run(app, host='0.0.0.0', port='8000', reloader=True)

'''