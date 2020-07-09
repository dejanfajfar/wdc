import unittest

from wdc.helper.time import WdcTime


class WdcTimeFixture(unittest.TestCase):
    def setUp(self):
        self.time = WdcTime("1240")

    def test_minutes(self):
        self.assertEqual("40", self.time.minutes)

        self.time = WdcTime("1300")
        self.assertEqual("00", self.time.minutes)

    def test_hours(self):
        self.assertEqual("12", self.time.hours)

    def test_init(self):
        # Upper out of bounds
        self.assertRaises(ValueError, WdcTime, "2360")

        # maximal numer of minutes is 59 so this time is invalid
        self.assertRaises(ValueError, WdcTime, "1260")

        # min valid time value
        self.assertTrue(WdcTime("0000"))

        # maximal valid time value
        self.assertTrue(WdcTime("2359"))

    def test_add(self):
        start_time = WdcTime("0800")
        end_time = WdcTime("0030")

        sum_time = start_time + end_time

        self.assertEqual("08", sum_time.hours)
        self.assertEqual("30", sum_time.minutes)

    def test_add_hours_stays_in_same_day(self):
        test_object = WdcTime("0800")
        test_object.add_hours(5)
        self.assertEqual(test_object.hours, "13")

    def test_add_hours_next_day(self):
        test_object = WdcTime("1300")
        test_object.add_hours(13)
        self.assertEqual(test_object.hours, "02")

    def test_add_hours_midnight(self):
        test_object = WdcTime("1200")
        test_object.add_hours(12)
        self.assertEqual(test_object.hours, "00")

    def test_add_hours_negative_hours(self):
        test_object = WdcTime("1200")
        test_object.add_hours(-3)
        self.assertEqual(test_object.hours, "09")

    def test_add_minutes(self):
        test_object = WdcTime("0800")
        test_object.add_minutes(30)
        self.assertEqual(test_object.minutes, "30")

    def test_add_minutes_carry_the_hour(self):
        test_object = WdcTime("0830")
        test_object.add_minutes(31)
        self.assertEqual(test_object.minutes, "01")
        self.assertEqual(test_object.hours, "09")

    def test_to_string(self):
        test_object = WdcTime("0835")
        self.assertEqual(test_object.__str__(), "0835")
