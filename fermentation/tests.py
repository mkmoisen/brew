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
            self.schedule = Schedule('2015-01-01 00:00:00', 50, [ScheduleIncrease(hours=5*24,temp=55),
                            ScheduleIncrease(hours=5*24 + 12*1,temp=60),
                            ScheduleIncrease(hours=5*24 + 12*2,temp=65),
                            ScheduleIncrease(hours=5*24 + 12*2 + 5*24,temp=60),
                            ScheduleIncrease(hours=5*24 + 12*2 + 5*24 + 12*1,temp=55),
                            ScheduleIncrease(hours=5*24 + 12*2 + 5*24 + 12*2,temp=50),
                            ScheduleIncrease(hours=5*24 + 12*2 + 5*24 + 12*3,temp=45),
                            ScheduleIncrease(hours=5*24 + 12*2 + 5*24 + 12*4,temp=40),
                            ScheduleIncrease(hours=5*24 + 12*2 + 5*24 + 12*5,temp=35),])
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

from fermentation.fermentation import Schedule, ScheduleIncrease
schedule = Schedule('2015-01-01 00:00:00', 50, [ScheduleIncrease(hours=5*24,temp=55),
                            ScheduleIncrease(hours=5*24 + 12*1,temp=60),
                            ScheduleIncrease(hours=5*24 + 12*2,temp=65),
                            ScheduleIncrease(hours=5*24 + 12*2 + 5*24,temp=60),
                            ScheduleIncrease(hours=5*24 + 12*2 + 5*24 + 12*1,temp=55),
                            ScheduleIncrease(hours=5*24 + 12*2 + 5*24 + 12*2,temp=50),
                            ScheduleIncrease(hours=5*24 + 12*2 + 5*24 + 12*3,temp=45),
                            ScheduleIncrease(hours=5*24 + 12*2 + 5*24 + 12*4,temp=40),
                            ScheduleIncrease(hours=5*24 + 12*2 + 5*24 + 12*5,temp=35),])

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

class TestPropertiesSql(unittest.TestCase):
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
from fermentation.tests import TestPropertiesSql
suite = unittest.TestLoader().loadTestsFromTestCase(TestPropertiesSql)
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


'''



class TestAngularFermentor(unittest.TestCase):
    def setUp(self):
        tables = [FermentationHost, FermentationFermentor, FermentationProbe, FermentationFermwrap, \
    FermentationTemperature, FermentationSchedule]
        self.tables = tables
        for table in tables:
            get_db().drop_table(table, True)
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
    '''
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
        '''


'''

import unittest
from fermentation.tests import TestAngularFermentor
suite = unittest.TestLoader().loadTestsFromTestCase(TestAngularFermentor)
unittest.TextTestRunner(verbosity=2).run(suite)

'''