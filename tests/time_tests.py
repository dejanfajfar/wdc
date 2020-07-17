import unittest
from freezegun import freeze_time
from wdc.time import WdcTime, is_time_valid, today, is_date_valid, to_date_no_day, timestamp


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

    @freeze_time('2020-10-25 15:16')
    def test_now_two_digit(self):
        test_object = WdcTime.now()
        self.assertEqual('1516', str(test_object))

    @freeze_time('2020-10-25 08:08')
    def test_now_one_digit(self):
        test_object = WdcTime.now()
        self.assertEqual('0808', str(test_object))


class IsTimeValidFixture(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(is_time_valid("0800"))
        self.assertTrue(is_time_valid("0000"))
        self.assertTrue(is_time_valid("2359"))

    def test_invalid(self):
        self.assertFalse(is_time_valid("2400"))
        self.assertFalse(is_time_valid("2360"))
        self.assertFalse(is_time_valid("9999"))


class TodayFixture(unittest.TestCase):
    @freeze_time('2019-10-25')
    def test_correct_format(self):
        test_result = today()
        self.assertEqual('2019-10-25', test_result)


class IsDateValidFixture(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(is_date_valid('2020-10-25'))
        self.assertTrue(is_date_valid('1980-07-01'))

    def test_invalid(self):
        self.assertFalse(is_date_valid('2000-7-1'))
        self.assertFalse(is_date_valid('1800-07-31'))
        self.assertFalse(is_date_valid('2000-40-01'))
        self.assertFalse(is_date_valid('2000-07-40'))
        self.assertFalse(is_date_valid(''))


class ToDateNoDayFixture(unittest.TestCase):
    def test_valid(self):
        test_result = to_date_no_day('2020-10-25')

        self.assertEqual('202010', test_result)

    def test_invalid_date_string(self):
        self.assertRaises(ValueError, to_date_no_day, '99')


class TimestampFixture(unittest.TestCase):
    @freeze_time('2020-10-25 10:00:00')
    def test_valid(self):
        test_object = timestamp()
        self.assertEqual('1603620000000', test_object)
