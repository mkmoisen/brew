__author__ = 'mmoisen'

import unittest
from fermentation import ScheduleIncrease, Schedule
from datetime import datetime, timedelta
from fermentation import FermentationHost, FermentationFermentor, FermentationProbe, FermentationFermwrap, \
    FermentationTemperature, FermentationSchedule
from fermentation import Properties
from settings import get_db
import socket
import json


class TestFermentation(unittest.TestCase):

    def setUp(self):
        pass

    def test_ScheduleIncrease_constructor_1(self):
        self.assertRaises(RuntimeError, ScheduleIncrease, {'hours':24,
                                                            'temp':68,
                                                            't':(24, 68)})

    def test_ScheduleIncrease_constructor_2(self):
        self.assertRaises(RuntimeError, ScheduleIncrease, {'hours':24,
                                                            't':(24, 68)})
    def test_ScheduleIncrease_constructor_3(self):
        self.assertRaises(RuntimeError, ScheduleIncrease, {'temp':68,
                                                            't':(24, 68)})
    def test_ScheduleIncrease_constructor_4(self):
        self.assertRaises(RuntimeError, ScheduleIncrease, {'hours':24})
    def test_ScheduleIncrease_constructor_1(self):
        self.assertRaises(RuntimeError, ScheduleIncrease, {'temp':68,})



class TestScheduleLager(unittest.TestCase):
    def setUp(self):
        if not hasattr(self, 'schedule'):
            self.schedule = Schedule('2015-01-01 00:00:00', 50, [
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24),temp=55),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*1),temp=60),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2),temp=65),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2 + 5*24),temp=60),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2 + 5*24 + 12*1),temp=55),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2 + 5*24 + 12*2),temp=50),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2 + 5*24 + 12*3),temp=45),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2 + 5*24 + 12*4),temp=40),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2 + 5*24 + 12*5),temp=35),
                            ]
            )
        if not hasattr(self, 'start_temp'):
            self.start_temp = 0


    def __init__(self, testName=None, schedule=None, start_temp=None):
        if testName is not None:
            super(TestScheduleLager, self).__init__(testName)
        else:
            super(TestScheduleLager, self).__init__()
        if schedule is not None:
            self.schedule = schedule
        if start_temp is not None:
            self.start_temp = 0

    def test_before_first_increase(self):

        today = '2015-01-05 23:59:59'
        today = datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
        self.assertEquals(self.start_temp, self.schedule.get_current_temp(today, self.start_temp))

    def test_6_0_increase(self):
        today = '2015-01-06 00:00:00'
        today = datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
        self.assertEquals(55, self.schedule.get_current_temp(today, self.start_temp))

    def test_before_6_12_increase(self):
        today = '2015-01-06 11:59:59'
        today = datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
        self.assertEquals(55, self.schedule.get_current_temp(today, self.start_temp))

    def test_6_12_increase(self):
        today = '2015-01-06 12:00:00'
        today = datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
        self.assertEquals(60, self.schedule.get_current_temp(today, self.start_temp))

    def test_before_7_0_increase(self):
        today = '2015-01-06 23:59:59'
        today = datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
        self.assertEquals(60, self.schedule.get_current_temp(today, self.start_temp))

    def test_7_0_increase(self):
        today = '2015-01-07 00:00:00'
        today = datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
        self.assertEquals(65, self.schedule.get_current_temp(today, self.start_temp))

    def test_before_12_00_increase_1(self):
        today = '2015-01-08 00:00:00'
        today = datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
        self.assertEquals(65, self.schedule.get_current_temp(today, self.start_temp))

    def test_before_12_00_increase_2(self):
        today = '2015-01-09 00:00:00'
        today = datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
        self.assertEquals(65, self.schedule.get_current_temp(today, self.start_temp))

    def test_before_12_00_increase_3(self):
        today = '2015-01-10 00:00:00'
        today = datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
        self.assertEquals(65, self.schedule.get_current_temp(today, self.start_temp))

    def test_before_12_00_increase_4(self):
        today = '2015-01-11 00:00:00'
        today = datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
        self.assertEquals(65, self.schedule.get_current_temp(today, self.start_temp))

    def test_before_12_00_increase_5(self):
        today = '2015-01-11 23:59:59'
        today = datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
        self.assertEquals(65, self.schedule.get_current_temp(today, self.start_temp))

    def test_12_0_increase(self):
        today = '2015-01-12 00:00:00'
        today = datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
        self.assertEquals(60, self.schedule.get_current_temp(today, self.start_temp))

    def test_before_12_12_increase(self):
        today = '2015-01-12 11:59:59'
        today = datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
        self.assertEquals(60, self.schedule.get_current_temp(today, self.start_temp))

    def test_12_12_increase(self):
        today = '2015-01-12 12:00:00'
        today = datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
        self.assertEquals(55, self.schedule.get_current_temp(today, self.start_temp))

    def test_before_13_0_increase(self):
        today = '2015-01-12 23:59:59'
        today = datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
        self.assertEquals(55, self.schedule.get_current_temp(today, self.start_temp))

    def test_13_0_increase(self):
        today = '2015-01-13 00:00:00'
        today = datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
        self.assertEquals(50, self.schedule.get_current_temp(today, self.start_temp))

    def test_before_13_12_increase(self):
        today = '2015-01-13 11:59:59'
        today = datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
        self.assertEquals(50, self.schedule.get_current_temp(today, self.start_temp))

    def test_13_12_increase(self):
        today = '2015-01-13 12:00:00'
        today = datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
        self.assertEquals(45, self.schedule.get_current_temp(today, self.start_temp))

    def test_before_14_0_increase(self):
        today = '2015-01-13 23:59:59'
        today = datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
        self.assertEquals(45, self.schedule.get_current_temp(today, self.start_temp))

    def test_14_0_increase(self):
        today = '2015-01-14 00:00:00'
        today = datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
        self.assertEquals(40, self.schedule.get_current_temp(today, self.start_temp))

    def test_before_14_12_increase(self):
        today = '2015-01-14 11:59:59'
        today = datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
        self.assertEquals(40, self.schedule.get_current_temp(today, self.start_temp))

    def test_14_12_increase(self):
        today = '2015-01-14 12:00:00'
        today = datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
        self.assertEquals(35, self.schedule.get_current_temp(today, self.start_temp))

    def test_after_14_12_increase_1(self):
        today = '2015-01-14 12:00:01'
        today = datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
        self.assertEquals(35, self.schedule.get_current_temp(today, self.start_temp))

    def test_after_14_12_increase_2(self):
        today = '2015-01-15 00:00:00'
        today = datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
        self.assertEquals(35, self.schedule.get_current_temp(today, self.start_temp))

    def test_after_14_12_increase_3(self):
        today = '2015-01-16 00:00:00'
        today = datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
        self.assertEquals(35, self.schedule.get_current_temp(today, self.start_temp))


from functools import partial
def getLagerSuite(schedule, start_temp):
    #suite = unittest.TestSuite()
    tests = ['test_before_first_increase',
                 'test_6_0_increase',
                 'test_before_6_12_increase',
                 'test_6_12_increase',
                 'test_before_7_0_increase',
                 'test_7_0_increase',
                 'test_before_12_00_increase_1',
                 'test_before_12_00_increase_2',
                 'test_before_12_00_increase_3',
                 'test_before_12_00_increase_4',
                 'test_before_12_00_increase_5',
                 'test_12_0_increase',
                 'test_before_12_12_increase',
                 'test_12_12_increase',
                 'test_before_13_0_increase',
                 'test_13_0_increase',
                 'test_before_13_12_increase',
                 'test_13_12_increase',
                 'test_before_14_0_increase',
                 'test_14_0_increase',
                 'test_before_14_12_increase',
                 'test_14_12_increase',
                 'test_after_14_12_increase_1',
                 'test_after_14_12_increase_2',
                 'test_after_14_12_increase_3']
    return unittest.TestSuite(map(partial(TestScheduleLager, schedule=schedule, start_temp=start_temp), tests))
'''

from datetime import datetime, timedelta
from fermentation.fermentation import Schedule, ScheduleIncrease
schedule = Schedule('2015-01-01 00:00:00', 50, [
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24),temp=55),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*1),temp=60),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2),temp=65),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2 + 5*24),temp=60),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2 + 5*24 + 12*1),temp=55),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2 + 5*24 + 12*2),temp=50),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2 + 5*24 + 12*3),temp=45),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2 + 5*24 + 12*4),temp=40),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2 + 5*24 + 12*5),temp=35),
                            ]
            )

import unittest
from fermentation.tests import getLagerSuite
suite = getLagerSuite(schedule=schedule, start_temp=0)
unittest.TextTestRunner(verbosity=2).run(suite)


#result = unittest.TestResult()
#suite.run(result)
#print result
#for error in result.errors:
#    print error
#schedule.increases
'''

'''
import unittest
from fermentation.tests import TestScheduleLager
suite = unittest.TestLoader().loadTestsFromTestCase(TestScheduleLager)
unittest.TextTestRunner(verbosity=2).run(suite)
'''










class TestScheduleAdjustment(unittest.TestCase):
    def setUp(self):
        pass

    def test_me_up(self):
        print "test_me_up\n"
        self.schedule = Schedule('2015-01-01 00:00:00', 50,
                                 [
                                     ScheduleIncrease(dt='2015-01-05T00:00:00', temp=55),
                                     ScheduleIncrease(dt='2015-01-05T12:00:00', temp=60),
                                     ScheduleIncrease(dt='2015-01-06T00:00:00', temp=65),
                                 ])

        for increase in self.schedule.increases:
            print increase

    def test_me_down(self):
        print "test_me_down\n"
        self.schedule = Schedule('2015-01-01 00:00:00', 50,
                                 [
                                     ScheduleIncrease(dt='2015-01-05T00:00:00', temp=45),
                                     ScheduleIncrease(dt='2015-01-05T12:00:00', temp=40),
                                     ScheduleIncrease(dt='2015-01-06T00:00:00', temp=35),
                                 ])

        for increase in self.schedule.increases:
            print increase

    def test_long_up(self):
        print 'test_long_up\n'
        self.schedule = Schedule('2015-01-01 00:00:00', 50,
                                 [
                                     ScheduleIncrease(dt='2015-01-05T00:00:00', temp=55),
                                     ScheduleIncrease(dt='2015-01-10T00:00:00', temp=60),
                                     ScheduleIncrease(dt='2015-01-15T00:00:00', temp=65),
                                 ])

        for increase in self.schedule.increases:
            print increase

    def test_long_down(self):
        print 'test_long_down\n'
        self.schedule = Schedule('2015-01-01 00:00:00', 50,
                                 [
                                     ScheduleIncrease(dt='2015-01-05T00:00:00', temp=45),
                                     ScheduleIncrease(dt='2015-01-10T00:00:00', temp=40),
                                     ScheduleIncrease(dt='2015-01-15T00:00:00', temp=35),
                                 ])

        for increase in self.schedule.increases:
            print increase

    def test_short_up(self):
        print 'test_short_up\n'
        self.schedule = Schedule('2015-01-01 00:00:00', 50,
                                 [
                                     ScheduleIncrease(dt='2015-01-05T00:00:00', temp=55),
                                     ScheduleIncrease(dt='2015-01-05T08:00:00', temp=60),
                                     ScheduleIncrease(dt='2015-01-05T16:00:00', temp=65),
                                 ])

        for increase in self.schedule.increases:
            print increase

    def test_short_down(self):
        print 'test_short_down\n'
        self.schedule = Schedule('2015-01-01 00:00:00', 50,
                                 [
                                     ScheduleIncrease(dt='2015-01-05T00:00:00', temp=45),
                                     ScheduleIncrease(dt='2015-01-05T08:00:00', temp=40),
                                     ScheduleIncrease(dt='2015-01-05T16:00:00', temp=35),
                                 ])

        for increase in self.schedule.increases:
            print increase

    def test_lager(self):
        print 'test_lager\n'
        self.schedule = Schedule('2015-01-01 00:00:00', 50, [
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24),temp=55),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*1),temp=60),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2),temp=65),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2 + 5*24),temp=60),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2 + 5*24 + 12*1),temp=55),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2 + 5*24 + 12*2),temp=50),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2 + 5*24 + 12*3),temp=45),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2 + 5*24 + 12*4),temp=40),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2 + 5*24 + 12*5),temp=35),
                            ]
            )
        for increase in self.schedule.increases:
            print increase
'''
import unittest
from fermentation.tests import TestScheduleAdjustment
suite = unittest.TestLoader().loadTestsFromTestCase(TestScheduleAdjustment)
unittest.TextTestRunner(verbosity=2).run(suite)
'''







class TestScheduleLagerAdjustment(unittest.TestCase):
    def setUp(self):
        if not hasattr(self, 'schedule'):
            self.schedule = Schedule('2015-01-01T00:00:00', 50, [
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24),temp=55),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*1),temp=60),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2),temp=65),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2 + 5*24),temp=60),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2 + 5*24 + 12*1),temp=55),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2 + 5*24 + 12*2),temp=50),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2 + 5*24 + 12*3),temp=45),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2 + 5*24 + 12*4),temp=40),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2 + 5*24 + 12*5),temp=35),
                            ]
            )
        if not hasattr(self, 'start_temp'):
            self.start_temp = 0


    def __init__(self, testName=None, schedule=None, start_temp=None):
        if testName is not None:
            super(TestScheduleLagerAdjustment, self).__init__(testName)
        else:
            super(TestScheduleLagerAdjustment, self).__init__()
        if schedule is not None:
            self.schedule = schedule
        if start_temp is not None:
            self.start_temp = 0

    def test_before_first_increase(self):

        today = '2015-01-05T23:59:59'
        today = datetime.strptime(today, '%Y-%m-%dT%H:%M:%S')
        self.assertEquals(self.start_temp, self.schedule.get_current_temp(today, self.start_temp))

    def test_6_0_increase(self):
        today = '2015-01-06T00:00:00'
        today = datetime.strptime(today, '%Y-%m-%dT%H:%M:%S')
        self.assertAlmostEquals(50+(55-50)/12.0, self.schedule.get_current_temp(today, self.start_temp), 7)
        #self.assertEquals(50+(55-50)/12.0, self.schedule.get_current_temp(today, self.start_temp))
        self.assertLess(self.schedule.get_current_temp(today, self.start_temp), 55)
        self.assertGreater(self.schedule.get_current_temp(today, self.start_temp),self.start_temp)

    def test_before_6_12_increase(self):
        today = '2015-01-06T11:59:59'
        today = datetime.strptime(today, '%Y-%m-%dT%H:%M:%S')
        self.assertEquals(55, self.schedule.get_current_temp(today, self.start_temp))

    def test_6_12_increase(self):
        today = '2015-01-06T12:00:00'
        today = datetime.strptime(today, '%Y-%m-%dT%H:%M:%S')
        #self.assertEquals(60, self.schedule.get_current_temp(today, self.start_temp))
        self.assertAlmostEquals(55+(60-55)/12.0, self.schedule.get_current_temp(today, self.start_temp), 7)
        self.assertLess(self.schedule.get_current_temp(today, self.start_temp), 60)
        self.assertGreater(self.schedule.get_current_temp(today, self.start_temp), 55)

    def test_before_7_0_increase(self):
        today = '2015-01-06T23:59:59'
        today = datetime.strptime(today, '%Y-%m-%dT%H:%M:%S')
        self.assertEquals(60, self.schedule.get_current_temp(today, self.start_temp))

    def test_7_0_increase(self):
        today = '2015-01-07T00:00:00'
        today = datetime.strptime(today, '%Y-%m-%dT%H:%M:%S')
        #self.assertEquals(65, self.schedule.get_current_temp(today, self.start_temp))
        self.assertAlmostEquals(60+(65-60)/12.0, self.schedule.get_current_temp(today, self.start_temp), 7)

    def test_before_12_00_increase_1(self):
        today = '2015-01-08T00:00:00'
        today = datetime.strptime(today, '%Y-%m-%dT%H:%M:%S')
        self.assertEquals(65, self.schedule.get_current_temp(today, self.start_temp))

    def test_before_12_00_increase_2(self):
        today = '2015-01-09T00:00:00'
        today = datetime.strptime(today, '%Y-%m-%dT%H:%M:%S')
        self.assertEquals(65, self.schedule.get_current_temp(today, self.start_temp))

    def test_before_12_00_increase_3(self):
        today = '2015-01-10T00:00:00'
        today = datetime.strptime(today, '%Y-%m-%dT%H:%M:%S')
        self.assertEquals(65, self.schedule.get_current_temp(today, self.start_temp))

    def test_before_12_00_increase_4(self):
        today = '2015-01-11T00:00:00'
        today = datetime.strptime(today, '%Y-%m-%dT%H:%M:%S')
        self.assertEquals(65, self.schedule.get_current_temp(today, self.start_temp))

    def test_before_12_00_increase_5(self):
        today = '2015-01-11T23:59:59'
        today = datetime.strptime(today, '%Y-%m-%dT%H:%M:%S')
        self.assertEquals(65, self.schedule.get_current_temp(today, self.start_temp))

    def test_12_0_increase(self):
        today = '2015-01-12T00:00:00'
        today = datetime.strptime(today, '%Y-%m-%dT%H:%M:%S')
        #self.assertEquals(60, self.schedule.get_current_temp(today, self.start_temp))
        self.assertAlmostEquals(65+(60-65)/12.0, self.schedule.get_current_temp(today, self.start_temp), 7)

    def test_before_12_12_increase(self):
        today = '2015-01-12T11:59:59'
        today = datetime.strptime(today, '%Y-%m-%dT%H:%M:%S')
        self.assertEquals(60, self.schedule.get_current_temp(today, self.start_temp))

    def test_12_12_increase(self):
        today = '2015-01-12T12:00:00'
        today = datetime.strptime(today, '%Y-%m-%dT%H:%M:%S')
        #self.assertEquals(55, self.schedule.get_current_temp(today, self.start_temp))
        self.assertAlmostEquals(60+(55-60)/12.0, self.schedule.get_current_temp(today, self.start_temp), 7)

    def test_before_13_0_increase(self):
        today = '2015-01-12T23:59:59'
        today = datetime.strptime(today, '%Y-%m-%dT%H:%M:%S')
        self.assertEquals(55, self.schedule.get_current_temp(today, self.start_temp))

    def test_13_0_increase(self):
        today = '2015-01-13T00:00:00'
        today = datetime.strptime(today, '%Y-%m-%dT%H:%M:%S')
        self.assertAlmostEquals(55+(50-55)/12.0, self.schedule.get_current_temp(today, self.start_temp),7)

    def test_before_13_12_increase(self):
        today = '2015-01-13T11:59:59'
        today = datetime.strptime(today, '%Y-%m-%dT%H:%M:%S')
        self.assertEquals(50, self.schedule.get_current_temp(today, self.start_temp))

    def test_13_12_increase(self):
        today = '2015-01-13T12:00:00'
        today = datetime.strptime(today, '%Y-%m-%dT%H:%M:%S')
        #self.assertEquals(45, self.schedule.get_current_temp(today, self.start_temp))
        self.assertAlmostEquals(50+(45-50)/12.0, self.schedule.get_current_temp(today, self.start_temp), 7)

    def test_before_14_0_increase(self):
        today = '2015-01-13T23:59:59'
        today = datetime.strptime(today, '%Y-%m-%dT%H:%M:%S')
        self.assertEquals(45, self.schedule.get_current_temp(today, self.start_temp))

    def test_14_0_increase(self):
        today = '2015-01-14T00:00:00'
        today = datetime.strptime(today, '%Y-%m-%dT%H:%M:%S')
        #self.assertEquals(40, self.schedule.get_current_temp(today, self.start_temp))
        self.assertAlmostEquals(45+(40-45)/12.0, self.schedule.get_current_temp(today, self.start_temp), 7)

    def test_before_14_12_increase(self):
        today = '2015-01-14T11:59:59'
        today = datetime.strptime(today, '%Y-%m-%dT%H:%M:%S')
        self.assertEquals(40, self.schedule.get_current_temp(today, self.start_temp))

    def test_14_12_increase(self):
        today = '2015-01-14T12:00:00'
        today = datetime.strptime(today, '%Y-%m-%dT%H:%M:%S')
        #self.assertEquals(35, self.schedule.get_current_temp(today, self.start_temp))
        self.assertAlmostEquals(40+(35-40)/12.0, self.schedule.get_current_temp(today, self.start_temp),7)

    def test_after_14_12_increase_1(self):
        today = '2015-01-15T00:00:00'
        today = datetime.strptime(today, '%Y-%m-%dT%H:%M:%S')
        self.assertEquals(35, self.schedule.get_current_temp(today, self.start_temp))

    def test_after_14_12_increase_2(self):
        today = '2015-01-16T00:00:00'
        today = datetime.strptime(today, '%Y-%m-%dT%H:%M:%S')
        self.assertEquals(35, self.schedule.get_current_temp(today, self.start_temp))


from functools import partial
def getLagerSuiteAdjustment(schedule, start_temp):
    #suite = unittest.TestSuite()
    tests = ['test_before_first_increase',
                 'test_6_0_increase',
                 'test_before_6_12_increase',
                 'test_6_12_increase',
                 'test_before_7_0_increase',
                 'test_7_0_increase',
                 'test_before_12_00_increase_1',
                 'test_before_12_00_increase_2',
                 'test_before_12_00_increase_3',
                 'test_before_12_00_increase_4',
                 'test_before_12_00_increase_5',
                 'test_12_0_increase',
                 'test_before_12_12_increase',
                 'test_12_12_increase',
                 'test_before_13_0_increase',
                 'test_13_0_increase',
                 'test_before_13_12_increase',
                 'test_13_12_increase',
                 'test_before_14_0_increase',
                 'test_14_0_increase',
                 'test_before_14_12_increase',
                 'test_14_12_increase',
                 'test_after_14_12_increase_1',
                 'test_after_14_12_increase_2',]
    return unittest.TestSuite(map(partial(TestScheduleLagerAdjustment, schedule=schedule, start_temp=start_temp), tests))
'''

from datetime import datetime, timedelta
from fermentation.fermentation import Schedule, ScheduleIncrease
schedule = Schedule('2015-01-01T00:00:00', 50, [
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24),temp=55),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*1),temp=60),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2),temp=65),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2 + 5*24),temp=60),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2 + 5*24 + 12*1),temp=55),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2 + 5*24 + 12*2),temp=50),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2 + 5*24 + 12*3),temp=45),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2 + 5*24 + 12*4),temp=40),
                            ScheduleIncrease(dt=datetime(2015,01,01,00,00,00) + timedelta(hours=5*24 + 12*2 + 5*24 + 12*5),temp=35),
                            ]
            )

import unittest
from fermentation.tests import getLagerSuiteAdjustment
suite = getLagerSuiteAdjustment(schedule=schedule, start_temp=0)
unittest.TextTestRunner(verbosity=2).run(suite)



'''































class TestPropertiesFromDb(unittest.TestCase):
    def setUp(self):
        tables = [FermentationHost, FermentationFermentor, FermentationProbe, FermentationFermwrap, \
    FermentationTemperature, FermentationSchedule]
        self.tables = tables
        for table in tables:
            table._meta.db_table += '_t'
            get_db().create_table(table, True)

    def test_one_host_one_fermentor(self):
        host = FermentationHost.create(hostname=socket.gethostname(),
                                       updated=0)
        fermentor = FermentationFermentor.create(name="Munich Dunkel",
                                                 start_date = datetime.now(),
                                                 end_begin_date = datetime.now() + timedelta(days=14),
                                                 end_end_date = datetime.now() + timedelta(days=21),
                                                 yeast = "Wyeast 2206",
                                                 og=1.050,
                                                 fg=None,
                                                 start_temp=50.0,
                                                 temp_differential=0.25,
                                                 active=1,
                                                 material="Glass",
                                                 host=host)
        fermwrap = FermentationFermwrap.create(pin=17,
                                               in_use=1,
                                               is_on=0,
                                               host=host,
                                               fermentor=fermentor)
        wort_probe = FermentationProbe.create(file_name='28-1234567890',
                                              type='wort',
                                              host=host,
                                              fermentor=fermentor)
        ambient_probe = FermentationProbe.create(file_name='28-0987654321',
                                                 type='ambient',
                                                 host=host,
                                                 fermentor=fermentor)
        schedule = [{'dt':datetime.strptime('2015-01-03 00:00:00', '%Y-%m-%d %H:%M:%S'), 'temp':55},
                    {'dt':datetime.strptime('2015-01-03 12:00:00', '%Y-%m-%d %H:%M:%S'), 'temp':60},
                    {'dt':datetime.strptime('2015-01-04 00:00:00', '%Y-%m-%d %H:%M:%S'), 'temp':65},]
        for sched in schedule:
            FermentationSchedule.create(fermentor=fermentor,
                                        dt=sched['dt'],
                                        temp=sched['temp'])

        expected_json = {"updated":0, "hostname":socket.gethostname(),
            "fermentors":[
                {"id":1,
                 "name":"Munich Dunkel",
                "start_temp":50.0,
                "temp_differential":0.25,
                "fermwrap_pin":17,
                "probes":[
                    {"file_name":"28-1234567890", "type":"wort"},
                    {"file_name":"28-0987654321", "type":"ambient"}
                ],
                "schedule": [
                    {"dt":"2015-01-03 00:00:00", "temp":55},
                    {"dt":"2015-01-03 12:00:00", "temp":60},
                    {"dt":"2015-01-04 00:00:00", "temp":65}
                    ]
                }
            ]
        }


        actual_json = Properties.read_properties_from_db()

        print "actual == \n", actual_json
        print "\n\nexpected == \n", expected_json

        self.assertEquals(expected_json, actual_json)

    def test_one_host_two_fermentors(self):
        host = FermentationHost.create(hostname=socket.gethostname(),
                                       updated=0)
        fermentor = FermentationFermentor.create(name="Munich Dunkel",
                                                 start_date = datetime.strptime('2015-01-03 00:00:00', '%Y-%m-%d %H:%M:%S'),
                                                 end_begin_date = datetime.strptime('2015-01-03 00:00:00', '%Y-%m-%d %H:%M:%S')+ timedelta(days=14),
                                                 end_end_date = datetime.strptime('2015-01-03 00:00:00', '%Y-%m-%d %H:%M:%S') + timedelta(days=21),
                                                 yeast = "Wyeast 2206",
                                                 og=1.050,
                                                 fg=None,
                                                 start_temp=50.0,
                                                 temp_differential=0.25,
                                                 active=1,
                                                 material="Glass",
                                                 host=host)
        fermwrap = FermentationFermwrap.create(pin=17,
                                               in_use=1,
                                               is_on=0,
                                               host=host,
                                               fermentor=fermentor)
        wort_probe = FermentationProbe.create(file_name='28-1234567890',
                                              type='wort',
                                              host=host,
                                              fermentor=fermentor)
        ambient_probe = FermentationProbe.create(file_name='28-0987654321',
                                                 type='ambient',
                                                 host=host,
                                                 fermentor=fermentor)
        schedule = [{'dt':datetime.strptime('2015-01-03 00:00:00', '%Y-%m-%d %H:%M:%S'), 'temp':55},
                    {'dt':datetime.strptime('2015-01-03 12:00:00', '%Y-%m-%d %H:%M:%S'), 'temp':60},
                    {'dt':datetime.strptime('2015-01-04 00:00:00', '%Y-%m-%d %H:%M:%S'), 'temp':65},]
        for sched in schedule:
            FermentationSchedule.create(fermentor=fermentor,
                                        dt=sched['dt'],
                                        temp=sched['temp'])

        fermentor = FermentationFermentor.create(name="Munich Helles",
                                                 start_date = datetime.now(),
                                                 end_begin_date = datetime.now() + timedelta(days=14),
                                                 end_end_date = datetime.now() + timedelta(days=21),
                                                 yeast = "Wyeast 2206",
                                                 og=1.060,
                                                 fg=None,
                                                 start_temp=52.0,
                                                 temp_differential=0.50,
                                                 active=1,
                                                 material="Glass",
                                                 host=host)
        fermwrap = FermentationFermwrap.create(pin=18,
                                               in_use=1,
                                               is_on=0,
                                               host=host,
                                               fermentor=fermentor)
        wort_probe = FermentationProbe.create(file_name='28-543219876',
                                              type='wort',
                                              host=host,
                                              fermentor=fermentor)
        ambient_probe = FermentationProbe.create(file_name='28-678954321',
                                                 type='ambient',
                                                 host=host,
                                                 fermentor=fermentor)
        schedule = [{'dt':datetime.strptime('2015-02-03 00:00:00', '%Y-%m-%d %H:%M:%S'), 'temp':57},
                    {'dt':datetime.strptime('2015-02-03 12:00:00', '%Y-%m-%d %H:%M:%S'), 'temp':62},
                    {'dt':datetime.strptime('2015-02-04 00:00:00', '%Y-%m-%d %H:%M:%S'), 'temp':67},]
        for sched in schedule:
            FermentationSchedule.create(fermentor=fermentor,
                                        dt=sched['dt'],
                                        temp=sched['temp'])

        expected_json = {"updated":0, "hostname":socket.gethostname(),
            "fermentors":[
                {"id":1,
                 "name":"Munich Dunkel",
                "start_temp":50.0,
                "temp_differential":0.25,
                "fermwrap_pin":17,
                "probes":[
                    {"file_name":"28-1234567890", "type":"wort"},
                    {"file_name":"28-0987654321", "type":"ambient"}
                ],
                "schedule": [
                    {"dt":"2015-01-03 00:00:00", "temp":55},
                    {"dt":"2015-01-03 12:00:00", "temp":60},
                    {"dt":"2015-01-04 00:00:00", "temp":65}
                    ]
                },
                {"id":2,
                 "name":"Munich Helles",
                "start_temp":52.0,
                "temp_differential":0.50,
                "fermwrap_pin":18,
                "probes":[
                    {"file_name":"28-543219876", "type":"wort"},
                    {"file_name":"28-678954321", "type":"ambient"}
                ],
                "schedule": [
                    {"dt":"2015-02-03 00:00:00", "temp":57},
                    {"dt":"2015-02-03 12:00:00", "temp":62},
                    {"dt":"2015-02-04 00:00:00", "temp":67}
                    ]
                }
            ]
        }


        from fermentation import Properties
        actual_json = Properties.read_properties_from_db()

        print "actual == \n", actual_json
        print "\n\nexpected == \n", expected_json

        self.assertEquals(expected_json, actual_json)

    def test_missing_probes(self):
        ''' Probes required'''
        host = FermentationHost.create(hostname=socket.gethostname(),
                                       updated=0)
        fermentor = FermentationFermentor.create(name="Munich Dunkel",
                                                 start_date = datetime.now(),
                                                 end_begin_date = datetime.now() + timedelta(days=14),
                                                 end_end_date = datetime.now() + timedelta(days=21),
                                                 yeast = "Wyeast 2206",
                                                 og=1.050,
                                                 fg=None,
                                                 start_temp=50.0,
                                                 temp_differential=0.25,
                                                 active=1,
                                                 material="Glass",
                                                 host=host)
        fermwrap = FermentationFermwrap.create(pin=17,
                                               in_use=1,
                                               is_on=0,
                                               host=host,
                                               fermentor=fermentor)

        self.assertRaises(RuntimeError, Properties.read_properties_from_db)

    def test_missing_ferwrap(self):
        '''Fermwrap not required'''
        host = FermentationHost.create(hostname=socket.gethostname(),
                                       updated=0)
        fermentor = FermentationFermentor.create(name="Munich Dunkel",
                                                 start_date = datetime.now(),
                                                 end_begin_date = datetime.now() + timedelta(days=14),
                                                 end_end_date = datetime.now() + timedelta(days=21),
                                                 yeast = "Wyeast 2206",
                                                 og=1.050,
                                                 fg=None,
                                                 start_temp=50.0,
                                                 temp_differential=0.25,
                                                 active=1,
                                                 material="Glass",
                                                 host=host)
        wort_probe = FermentationProbe.create(file_name='28-1234567890',
                                              type='wort',
                                              host=host,
                                              fermentor=fermentor)
        ambient_probe = FermentationProbe.create(file_name='28-0987654321',
                                                 type='ambient',
                                                 host=host,
                                                 fermentor=fermentor)


        print "missing fermwrap == {}".format(Properties.read_properties_from_db())

    def test_missing_schedule(self):
        '''Schedule not required'''
        host = FermentationHost.create(hostname=socket.gethostname(),
                                       updated=0)
        fermentor = FermentationFermentor.create(name="Munich Dunkel",
                                                 start_date = datetime.now(),
                                                 end_begin_date = datetime.now() + timedelta(days=14),
                                                 end_end_date = datetime.now() + timedelta(days=21),
                                                 yeast = "Wyeast 2206",
                                                 og=1.050,
                                                 fg=None,
                                                 start_temp=50.0,
                                                 temp_differential=0.25,
                                                 active=1,
                                                 material="Glass",
                                                 host=host)
        wort_probe = FermentationProbe.create(file_name='28-1234567890',
                                              type='wort',
                                              host=host,
                                              fermentor=fermentor)
        ambient_probe = FermentationProbe.create(file_name='28-0987654321',
                                                 type='ambient',
                                                 host=host,
                                                 fermentor=fermentor)
        fermwrap = FermentationFermwrap.create(pin=17,
                                               in_use=1,
                                               is_on=0,
                                               host=host,
                                               fermentor=fermentor)

        print "missing schedule == {}".format(Properties.read_properties_from_db())


    def tearDown(self):
        for table in self.tables:
            #reverse():
            get_db().drop_table(table)

'''

import unittest
from fermentation.tests import TestPropertiesFromDb
suite = unittest.TestLoader().loadTestsFromTestCase(TestPropertiesFromDb)
unittest.TextTestRunner(verbosity=2).run(suite)

'''

from fermentation_controller import get_active_fermentors

class TestBottleFermentor(unittest.TestCase):
    def setUp(self):
        tables = [FermentationHost, FermentationFermentor, FermentationProbe, FermentationFermwrap, \
    FermentationTemperature, FermentationSchedule]
        self.tables = tables
        for table in tables:
            table._meta.db_table += '_t'
            get_db().create_table(table, True)

    def test_one_fermentor(self):
        host = FermentationHost.create(hostname=socket.gethostname(),
                                       updated=0)
        fermentor = FermentationFermentor.create(name="Munich Dunkel",
                                                 start_date = datetime.now(),
                                                 end_begin_date = datetime.now() + timedelta(days=14),
                                                 end_end_date = datetime.now() + timedelta(days=21),
                                                 yeast = "Wyeast 2206",
                                                 og=1.050,
                                                 fg=None,
                                                 start_temp=50.0,
                                                 temp_differential=0.25,
                                                 active=1,
                                                 material="Glass",
                                                 host=host)
        fermwrap = FermentationFermwrap.create(pin=17,
                                               in_use=1,
                                               is_on=0,
                                               host=host,
                                               fermentor=fermentor)
        wort_probe = FermentationProbe.create(file_name='28-1234567890',
                                              type='wort',
                                              host=host,
                                              fermentor=fermentor)
        ambient_probe = FermentationProbe.create(file_name='28-0987654321',
                                                 type='ambient',
                                                 host=host,
                                                 fermentor=fermentor)
        schedule = [{'dt':datetime.strptime('2015-01-03 00:00:00', '%Y-%m-%d %H:%M:%S'), 'temp':55},
                    {'dt':datetime.strptime('2015-01-03 12:00:00', '%Y-%m-%d %H:%M:%S'), 'temp':60},
                    {'dt':datetime.strptime('2015-01-04 00:00:00', '%Y-%m-%d %H:%M:%S'), 'temp':65},]
        for sched in schedule:
            FermentationSchedule.create(fermentor=fermentor,
                                        dt=sched['dt'],
                                        temp=sched['temp'])

        get_active_fermentors()

    def test_two_fermentors(self):
        host = FermentationHost.create(hostname=socket.gethostname(),
                                       updated=0)
        fermentor = FermentationFermentor.create(name="Munich Dunkel",
                                                 start_date = datetime.strptime('2015-01-03 00:00:00', '%Y-%m-%d %H:%M:%S'),
                                                 end_begin_date = datetime.strptime('2015-01-03 00:00:00', '%Y-%m-%d %H:%M:%S')+ timedelta(days=14),
                                                 end_end_date = datetime.strptime('2015-01-03 00:00:00', '%Y-%m-%d %H:%M:%S') + timedelta(days=21),
                                                 yeast = "Wyeast 2206",
                                                 og=1.050,
                                                 fg=None,
                                                 start_temp=50.0,
                                                 temp_differential=0.25,
                                                 active=1,
                                                 material="Glass",
                                                 host=host)
        fermwrap = FermentationFermwrap.create(pin=17,
                                               in_use=1,
                                               is_on=0,
                                               host=host,
                                               fermentor=fermentor)
        wort_probe = FermentationProbe.create(file_name='28-1234567890',
                                              type='wort',
                                              host=host,
                                              fermentor=fermentor)
        ambient_probe = FermentationProbe.create(file_name='28-0987654321',
                                                 type='ambient',
                                                 host=host,
                                                 fermentor=fermentor)
        schedule = [{'dt':datetime.strptime('2015-01-03 00:00:00', '%Y-%m-%d %H:%M:%S'), 'temp':55},
                    {'dt':datetime.strptime('2015-01-03 12:00:00', '%Y-%m-%d %H:%M:%S'), 'temp':60},
                    {'dt':datetime.strptime('2015-01-04 00:00:00', '%Y-%m-%d %H:%M:%S'), 'temp':65},]
        for sched in schedule:
            FermentationSchedule.create(fermentor=fermentor,
                                        dt=sched['dt'],
                                        temp=sched['temp'])

        fermentor = FermentationFermentor.create(name="Munich Helles",
                                                 start_date = datetime.now(),
                                                 end_begin_date = datetime.now() + timedelta(days=14),
                                                 end_end_date = datetime.now() + timedelta(days=21),
                                                 yeast = "Wyeast 2206",
                                                 og=1.060,
                                                 fg=None,
                                                 start_temp=52.0,
                                                 temp_differential=0.50,
                                                 active=1,
                                                 material="Glass",
                                                 host=host)
        fermwrap = FermentationFermwrap.create(pin=18,
                                               in_use=1,
                                               is_on=0,
                                               host=host,
                                               fermentor=fermentor)
        wort_probe = FermentationProbe.create(file_name='28-543219876',
                                              type='wort',
                                              host=host,
                                              fermentor=fermentor)
        ambient_probe = FermentationProbe.create(file_name='28-678954321',
                                                 type='ambient',
                                                 host=host,
                                                 fermentor=fermentor)
        schedule = [{'dt':datetime.strptime('2015-02-03 00:00:00', '%Y-%m-%d %H:%M:%S'), 'temp':57},
                    {'dt':datetime.strptime('2015-02-03 12:00:00', '%Y-%m-%d %H:%M:%S'), 'temp':62},
                    {'dt':datetime.strptime('2015-02-04 00:00:00', '%Y-%m-%d %H:%M:%S'), 'temp':67},]
        for sched in schedule:
            FermentationSchedule.create(fermentor=fermentor,
                                        dt=sched['dt'],
                                        temp=sched['temp'])

        get_active_fermentors()

    def tearDown(self):
        for table in self.tables:
            #reverse():
            get_db().drop_table(table)

'''

import unittest
from fermentation.tests import TestBottleFermentor
suite = unittest.TestLoader().loadTestsFromTestCase(TestBottleFermentor)
unittest.TextTestRunner(verbosity=2).run(suite)

'''
'''
import peewee
from settings import BaseModel, get_db

from fermentation.fermentation import FermentationHost, FermentationFermentor, FermentationProbe, FermentationFermwrap
from fermentation.fermentation import FermentationSchedule

d_fermentors = FermentationFermentor.select()
d_hosts = FermentationFermentor.select()

for fermentor in peewee.prefetch(FermentationHost.select(), FermentationFermentor):
    print fermentor.hostname

for host in peewee.prefetch(FermentationHost.select(), FermentationFermentor.select(), FermentationProbe.select(), FermentationFermwrap.select(), FermentationSchedule.select()):
    print host.hostname
    for fermentor in host.host_fermentors:
        print "\t",fermentor.name
        for probe in fermentor.fermentor_probes:
            print "\t",probe.file_name
        for fermwrap in fermentor.fermentor_fermwraps:
            print "\t",fermwrap.pin
        for schedule in fermentor.fermentor_schedules:
            print "\t",schedule.dt, schedule.temp


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

query = (FermentationFermentor.select(FermentationFermentor, FermentationProbe).join(FermentationProbe)).aggregate_rows()

for fermentor in query:
    print fermentor.name


class Parent(BaseModel):
    name = peewee.CharField()

class Child(BaseModel):
    name = peewee.CharField()
    parent = peewee.ForeignKeyField(Parent, related_name='children')

db = get_db()

db.create_table(Parent)
db.create_table(Child)

parent = Parent.create(name="Parent1")
child1 = Child.create(name="Child1", parent=parent)
chilld2 = Child.create(name="Child2", parent=parent)

query = (Parent.select(Parent, Child)
        .join(Child))

pars = []

for p in query:
    if p not in pars:
        pars.append(p)
    print p.name
    for c in p.children:
        print "\t",c.name

print "\n\n does it work?"
for p in pars:
    print p.name
    for c in p.children:
        print "\t",c.name

for parent in peewee.prefetch(Parent.select(), Child.select().where(Child.name=='Child2')):
    print parent.name
    for child in parent.children:
        print child.name

query = (Parent.select(Parent, Child)
        .join(Child)).aggregate_rows()

for parent in query:
    print parent.name
    for child in parent.children:
        print child.name


'''



class TestAngularFermentor(unittest.TestCase):
    def setUp(self):
        tables = [FermentationHost, FermentationFermentor, FermentationProbe, FermentationFermwrap, \
            FermentationTemperature, FermentationSchedule]
        for table in tables:
            table._meta.db_table += '_t'
        from init_db import drop_and_create_tables

        drop_and_create_tables()


    def test_one_fermentor(self):
        host = FermentationHost.get(FermentationHost.hostname=='mmoisen-WS')

        fermentor = FermentationFermentor.create(name="Munich Dunkel",
                                                 start_date = datetime.now(),
                                                 end_begin_date = datetime.now() + timedelta(days=14),
                                                 end_end_date = datetime.now() + timedelta(days=21),
                                                 yeast = "Wyeast 2206",
                                                 og=1.050,
                                                 fg=None,
                                                 start_temp=50.0,
                                                 temp_differential=0.25,
                                                 active=1,
                                                 material="Glass",
                                                 host=host)

        fermwrap = FermentationFermwrap.get(FermentationFermwrap.host==host, FermentationFermwrap.pin==17)
        print "LOL fermwrap host is ", fermwrap.host.id, fermwrap.pin
        fermwrap.fermentor=fermentor
        fermwrap.in_use = 1
        print "LOL fermwrap host is ", fermwrap.host.id, fermwrap.pin, fermwrap.fermentor.name
        fermwrap.save()
        print "LOL fermwrap host is ", fermwrap.host.id, fermwrap.pin, fermwrap.fermentor.name
        wort_probe = FermentationProbe.create(file_name='28-1234567890',
                                              type='wort',
                                              in_use=1,
                                              host=host,
                                              fermentor=fermentor)
        ambient_probe = FermentationProbe.create(file_name='28-0987654321',
                                                 type='ambient',
                                                 host=host,
                                                 in_use=1,
                                                 fermentor=fermentor)
        schedule = [{'dt':datetime.strptime('2015-01-03 00:00:00', '%Y-%m-%d %H:%M:%S'), 'temp':55},
                    {'dt':datetime.strptime('2015-01-03 12:00:00', '%Y-%m-%d %H:%M:%S'), 'temp':60},
                    {'dt':datetime.strptime('2015-01-04 00:00:00', '%Y-%m-%d %H:%M:%S'), 'temp':65},]
        for sched in schedule:
            FermentationSchedule.create(fermentor=fermentor,
                                        dt=sched['dt'],
                                        temp=sched['temp'])

        get_active_fermentors()
    '''
    def test_two_fermentors(self):
        host = FermentationHost.get(FermentationHost.hostname='mmoisen-WS'))
        fermentor = FermentationFermentor.create(name="Munich Dunkel",
                                                 start_date = datetime.strptime('2015-01-03 00:00:00', '%Y-%m-%d %H:%M:%S'),
                                                 end_begin_date = datetime.strptime('2015-01-03 00:00:00', '%Y-%m-%d %H:%M:%S')+ timedelta(days=14),
                                                 end_end_date = datetime.strptime('2015-01-03 00:00:00', '%Y-%m-%d %H:%M:%S') + timedelta(days=21),
                                                 yeast = "Wyeast 2206",
                                                 og=1.050,
                                                 fg=None,
                                                 start_temp=50.0,
                                                 temp_differential=0.25,
                                                 active=1,
                                                 material="Glass",
                                                 host=host)
        fermwrap = FermentationFermwrap.create(pin=17,
                                               in_use=1,
                                               is_on=0,
                                               host=host,
                                               fermentor=fermentor)
        wort_probe = FermentationProbe.create(file_name='28-1234567890',
                                              type='wort',
                                              host=host,
                                              fermentor=fermentor)
        ambient_probe = FermentationProbe.create(file_name='28-0987654321',
                                                 type='ambient',
                                                 host=host,
                                                 fermentor=fermentor)
        schedule = [{'dt':datetime.strptime('2015-01-03 00:00:00', '%Y-%m-%d %H:%M:%S'), 'temp':55},
                    {'dt':datetime.strptime('2015-01-03 12:00:00', '%Y-%m-%d %H:%M:%S'), 'temp':60},
                    {'dt':datetime.strptime('2015-01-04 00:00:00', '%Y-%m-%d %H:%M:%S'), 'temp':65},]
        for sched in schedule:
            FermentationSchedule.create(fermentor=fermentor,
                                        dt=sched['dt'],
                                        temp=sched['temp'])

        fermentor = FermentationFermentor.create(name="Munich Helles",
                                                 start_date = datetime.now(),
                                                 end_begin_date = datetime.now() + timedelta(days=14),
                                                 end_end_date = datetime.now() + timedelta(days=21),
                                                 yeast = "Wyeast 2206",
                                                 og=1.060,
                                                 fg=None,
                                                 start_temp=52.0,
                                                 temp_differential=0.50,
                                                 active=1,
                                                 material="Glass",
                                                 host=host)
        fermwrap = FermentationFermwrap.create(pin=18,
                                               in_use=1,
                                               is_on=0,
                                               host=host,
                                               fermentor=fermentor)
        wort_probe = FermentationProbe.create(file_name='28-543219876',
                                              type='wort',
                                              host=host,
                                              fermentor=fermentor)
        ambient_probe = FermentationProbe.create(file_name='28-678954321',
                                                 type='ambient',
                                                 host=host,
                                                 fermentor=fermentor)
        schedule = [{'dt':datetime.strptime('2015-02-03 00:00:00', '%Y-%m-%d %H:%M:%S'), 'temp':57},
                    {'dt':datetime.strptime('2015-02-03 12:00:00', '%Y-%m-%d %H:%M:%S'), 'temp':62},
                    {'dt':datetime.strptime('2015-02-04 00:00:00', '%Y-%m-%d %H:%M:%S'), 'temp':67},]
        for sched in schedule:
            FermentationSchedule.create(fermentor=fermentor,
                                        dt=sched['dt'],
                                        temp=sched['temp'])

        get_active_fermentors()
        '''


'''

import unittest
from fermentation.tests import TestAngularFermentor
suite = unittest.TestLoader().loadTestsFromTestCase(TestAngularFermentor)
unittest.TextTestRunner(verbosity=2).run(suite)

'''

from fermentation import FermentationFermwrapHistory, Fermentor

import time

class TestFermwrapHistory(unittest.TestCase):
    def setUp(self):
        FermentationFermwrapHistory._meta.db_table += '_t'
        get_db().drop_table(FermentationFermwrapHistory,True)
        get_db().create_table(FermentationFermwrapHistory, True)
        FermentationFermentor.create(name="hai",
                                     start_date=datetime.now(),
                                     start_temp=50,
                                     temp_differential=0.125,
                                     active=1,
                                     material='glass',
                                     host=1)


    def test_lol(self):
        fermentor = Fermentor(
            name='Test FHistory',
            start_temp=50,
            temp_differential=0.125,
            fermwrap_pin=17,
            id=1
        )
        self.assertEquals(fermentor.is_fermwrap, True)
        self.assertEquals(fermentor.is_fermwrap_on, False)
        self.assertEquals(hasattr(fermentor, 'dt_fermwrap_turned_on'), False)
        self.assertEquals(hasattr(fermentor, 'dt_fermwrap_turned_off'), False)

        # Turn fermwrap on the first time
        dt = datetime(2015,01,01,00,00,00)
        # Verify fermwrap_turned_on_now = True
        self.assertEquals(fermentor.turn_fermwrap_on(dt), True)
        dt_fermwrap_turned_on = fermentor.dt_fermwrap_turned_on
        self.assertNotEquals(fermentor.dt_fermwrap_turned_on, None)
        self.assertEquals(fermentor.dt_fermwrap_turned_off, None)
        self.assertEquals(fermentor.target_temp_at_start, fermentor.target_temp)
        self.assertEquals(fermentor.is_fermwrap_on, True)

        # Call fermwrap on a second time
        dt = datetime(2015, 01, 01, 00, 10, 00)
        # verify fermwrap_turned_on_now = False
        self.assertEquals(fermentor.turn_fermwrap_on(dt), False)
        self.assertNotEquals(fermentor.dt_fermwrap_turned_on, None)
        self.assertEquals(fermentor.dt_fermwrap_turned_off, None)
        self.assertEquals(dt_fermwrap_turned_on, fermentor.dt_fermwrap_turned_on)
        self.assertEquals(fermentor.target_temp_at_start, fermentor.target_temp)
        self.assertEquals(fermentor.is_fermwrap_on, True)

        time.sleep(2)
        # XCall fermwrap off first time
        dt = datetime(2015, 01, 01, 00, 20, 00)
        # verify fermwrap_turned_off_now = True
        self.assertEquals(fermentor.turn_fermwrap_off(dt), True)
        self.assertNotEquals(fermentor.dt_fermwrap_turned_off, None)
        self.assertEquals(fermentor.dt_fermwrap_turned_on, None)
        self.assertEquals(fermentor.target_temp_at_start, fermentor.target_temp)
        self.assertEquals(fermentor.is_fermwrap_on, False)

        # Call fermwrap off second time
        dt = datetime(2015, 01, 01, 00, 30, 00)
        self.assertEquals(fermentor.turn_fermwrap_off(dt), False)
        self.assertNotEquals(fermentor.dt_fermwrap_turned_off, None)
        self.assertEquals(fermentor.dt_fermwrap_turned_on, None)
        self.assertEquals(fermentor.is_fermwrap_on, False)

        time.sleep(2)
        # Call fermwrap on third time
        dt = datetime(2015, 01, 01, 00, 30, 00)
        self.assertEquals(fermentor.turn_fermwrap_on(dt), True)
        self.assertNotEquals(fermentor.dt_fermwrap_turned_on, None)
        self.assertEquals(fermentor.dt_fermwrap_turned_off, None)



'''
import unittest
from fermentation.tests import TestFermwrapHistory
suite = unittest.TestLoader().loadTestsFromTestCase(TestFermwrapHistory)
unittest.TextTestRunner(verbosity=2).run(suite)
'''