import unittest

from wdc.calculator import calc_workday_end

class CalcualtorFixture(unittest.TestCase):
    def test_valid_scenarios(self):
        result = calc_workday_end('0800', 30, '0800')
        self.assertEqual(str(result), '1630')
