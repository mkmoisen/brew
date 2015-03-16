#!/usr/bin/python
import os
import glob
import time
from datetime import datetime
import datetime
import traceback
import decimal


from models import Probe, PowerSwitchTail2, Heater

class Pump(PowerSwitchTail2):
    pass


class Heating(object):
    def __init__(self, heaters=[]):
        assert isinstance(heaters, list)
        for heater in heaters:
            assert isinstance(heater, Heater)
        self.heaters = heaters
        self.is_on = False

    def turn_on(self):
        [heater.turn_on() for heater in self.heaters]
        self.is_on = True

    def turn_off(self):
        [heater.turn_off() for heater in self.heaters]
        self.is_on = False

    def __str__(self):
        return "\n".join([str(heater) for heater in self.heaters])

    def __repr__(self):
        return "Heating(heaters=[" + ",".join([repr(heater) for heater in self.heaters]) + "])"

class Step(object):
    def __init__(self, name, duration, temp):
        self.name = name
        self.duration = duration
        self.temp = float(temp)

        self.min_temp = self.temp - 0.5
        self.max_temp = self.temp + 0.5

    @property
    def time_elapsed(self):
        if not hasattr(self, 'start_time'):
            # Step hasn't started yet
            return 0

        return (time.time() - self.start_time) / 60.0

    def __str__(self):
        return "name = {}, duration = {}, temp = {}".format(self.name, self.duration, self.temp)

    def __repr__(self):
        return "Step(name='{}', duration={}, temp={})".format(self.name, self.duration, self.temp)



class Herms(object):
    def __init__(self, hlt_probe, mashtun_probe, heating, pump, steps=[], room_temp=70, water_grist_ratio=1.25):
        assert isinstance(hlt_probe, Probe)
        assert isinstance(mashtun_probe, Probe)
        assert isinstance(heating, Heating)
        assert isinstance(steps, list)
        self.hlt_probe = hlt_probe
        self.mashtun_probe = mashtun_probe
        self.heating = heating
        self.pump = pump
        self.steps = steps
        self.current_step_index = -1 # Use next_step() to go to first step
        self.current_step = steps[0]
        self.temp_history = {}
        self.initialized_strike_water = False
        # There may be a period of time after strike water is ready and user has completed the strike
        self.strike_completed = False
        # Strike Ready is intermediate step before strike completed which just stops the pump so user can strike
        self.strike_ready = False
        self.room_temp = room_temp
        self.water_grist_ratio = water_grist_ratio
        self.strike_water_temp = self._calculate_strike_water_temp()
        self.mash_complete = False
        self.data = [] # Data for mash temps
        self.strike_data = [] # Data for warming up strike water only


    def __str__(self):
        return "{}\n{}\n{}\n{}\n".format(self.hlt_probe, self.mashtun_probe, self.heating, self.steps)

    def __repr__(self):
        return "Herms(hlt_probe={}, mashtun_probe={}, heating={}".format(repr(self.hlt_probe), repr(self.mashtun_probe),
                                                                         repr(self.heating)) + \
               ", steps=[" + ",".join([repr(step) for step in self.steps]) + '])'

    def _calculate_strike_water_temp(self):
       return (0.2/self.water_grist_ratio) * (self.steps[0].temp - self.room_temp) + (self.steps[0].temp)


    @property
    def time_elapsed(self):
        return (time.time() - self.start_time) / 60.0

    @property
    def strike_time_elapsed(self):
        return (time.time() - self.strike_start_time) / 60.0

    @property
    def hlt_temp(self):
        return self.hlt_probe.temp

    @property
    def mashtun_temp(self):
        return self.mashtun_probe.temp


    def initialize_strike_water(self):
        self.strike_start_time = time.time()

        self.pump.turn_on()

        while not self.strike_ready:

            # Read temps
            hlt_temp = self.hlt_probe.temp
            mashtun_temp = self.mashtun_probe.temp

            # Add it to data set
            self.stirke_data.append([self.time_elapsed, hlt_temp, mashtun_temp])

            # Adjust temperature if necessary
            if hlt_temp < self.strike_water_temp:
                if not self.pump.is_on:
                    self.pump.turn_on()
                self.heating.turn_on()
                self.initialized_strike_water = False
            elif hlt_temp >= self.strike_water_temp:
                self.heating.turn_off()
                if self.pump.is_on():
                    self.pump.turn_off()
                self.initialized_strike_water = True

            time.sleep(5)

        # remove this function as it should no longer be called
        del self.initialize_strike_water

        return

    def _next_step(self):
        self.current_step_index += 1
        self.current_step = self.steps[self.current_step_index]

        # Start individual Step's duration timer
        self.current_step.start_time = time.time()

        # Start pump in the event it was off during the Strike/first step
        self.pump.turn_on()

    def run(self):
        if not self.strike_completed:
            raise RuntimeError("Don't execute brew.run() unless strike is completed.")

        # Start Total Duration
        self.start_time = time.time()

        # Advance to first step (sets current_step_index to 0)
        self._next_step()

        while True:
            # Check to see if next step is ready
            if self.current_step.time_elapsed > self.current_step.duration:
                if len(self.steps) == self.current_step_index + 1:
                    # This is the last step. Time to Sparge
                    self.mash_complete = True
                    return
                else:
                    # Move to next step
                    self._next_step()

            # Read temps
            hlt_temp = self.hlt_probe.temp
            mashtun_temp = self.mashtun_probe.temp

            # Add it to data set
            self.data.append([self.time_elapsed, hlt_temp, mashtun_temp])

            # Adjust temperature if necessary
            if hlt_temp >= self.current_step.max_temp:
                self.heating.turn_off()
                # For first step, HLT water will be at strike water temp, so turn off pump while HLT is cooling down
                # This could also do the same for all steps, perhaps?
                if self.current_step_index == 0:
                    if self.pump.is_on():
                        self.pump.turn_off()
            elif hlt_temp < self.current_step.min_temp:
                self.heating.turn_on()
                # For first step, HLT water will be at strike water temp, so turn off pump while HLT is cooling down
                # This could also do the same for all steps, perhaps?
                if self.current_step_index == 0:
                    if not self.pump.is_on():
                        self.pump.turn_on()

            # Sleep
            time.sleep(5)

