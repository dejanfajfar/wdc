import unittest

from wdc.classes import WdcTimeSlotDuration, WdcTimeSlot
from wdc.time import WdcTime


class DurationTests(unittest.TestCase):
    def test_duration(self):
        duration = WdcTimeSlotDuration(WdcTimeSlot(WdcTime('0800'), WdcTime('0932')))

        self.assertEqual(1, duration.hours)
        self.assertEqual(32, duration.minutes)

    def test_duration_str_format(self):
        duration = WdcTimeSlotDuration(WdcTimeSlot(WdcTime('0800'), WdcTime('0932')))

        self.assertEqual('01:32', duration.time_str())
        self.assertEqual('1.53', duration.time_fraction_str())
