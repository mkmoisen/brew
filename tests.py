__author__ = 'mmoisen'

import unittest

import fermentation.tests


suite = unittest.TestLoader().loadTestsFromTestCase(fermentation.tests.TestFermentation)
unittest.TextTestRunner(verbosity=2).run(suite)

suite = unittest.TestLoader().loadTestsFromTestCase(fermentation.tests.TestScheduleLager)
unittest.TextTestRunner(verbosity=2).run(suite)














from herms.herms import *


'''
class TestCalculateStrikeWaterTemp(unittest.TestCase):
    herms = None

    def setUp(self):
        TestCalculateStrikeWaterTemp.herms = Herms.__new__(Herms)

    def test_(self):
        TestCalculateStrikeWaterTemp.herms.room_temp = 70
        TestCalculateStrikeWaterTemp.herms.water_grist_ratio = 1.25
        TestCalculateStrikeWaterTemp.herms.steps = [Step("sacc",60,154)]
        strike_water_temp = TestCalculateStrikeWaterTemp.herms._calculate_strike_water_temp()
        self.assertEqual(strike_water_temp, 167.44)

if __name__ == '__main__':
    unittest.main()
'''