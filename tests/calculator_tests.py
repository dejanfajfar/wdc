import unittest

from wdc.calculator import calc_workday_end


class CalcualtorFixture(unittest.TestCase):
    def test_valid_scenarios(self):
        scenarios = [
            ('0800', 30, '0800', '1630'),
            ('0800', 30, '0745', '1615'),
            ('0800', 0, '0745', '1545'),
            ('0800', 60, '0745', '1645'),
        ]

        for scenario in scenarios:
            with self.subTest(scenario):
                result = calc_workday_end(scenario[0], scenario[1], scenario[2])
                self.assertEqual(str(result), scenario[3])
