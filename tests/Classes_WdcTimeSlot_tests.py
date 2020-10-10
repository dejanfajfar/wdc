import unittest

from wdc.classes import WdcTimeSlot, WdcTimeSlotComparison
from wdc.time import WdcTime


class CompareWith(unittest.TestCase):
    def test_overlapping(self):
        slot1 = WdcTimeSlot(start=WdcTime('0800'), end=WdcTime('0900'))
        slot2 = WdcTimeSlot(start=WdcTime('0830'), end=WdcTime('0930'))

        self.assertEqual(slot1.compare_with(slot2), WdcTimeSlotComparison.OVERLAP)

    def test_same(self):
        slot1 = WdcTimeSlot(start=WdcTime('0800'), end=WdcTime('0900'))

        self.assertEqual(slot1.compare_with(slot1), WdcTimeSlotComparison.OVERLAP)

    def test_before_not_touching(self):
        slot1 = WdcTimeSlot(start=WdcTime('0800'), end=WdcTime('0900'))
        slot2 = WdcTimeSlot(start=WdcTime('0600'), end=WdcTime('0700'))

        self.assertEqual(slot1.compare_with(slot2), WdcTimeSlotComparison.AFTER)

    def test_before_touching(self):
        slot1 = WdcTimeSlot(start=WdcTime('0800'), end=WdcTime('0900'))
        slot2 = WdcTimeSlot(start=WdcTime('0700'), end=WdcTime('0800'))

        self.assertEqual(slot1.compare_with(slot2), WdcTimeSlotComparison.AFTER)

    def test_after_not_touching(self):
        slot1 = WdcTimeSlot(start=WdcTime('0800'), end=WdcTime('0900'))
        slot2 = WdcTimeSlot(start=WdcTime('1000'), end=WdcTime('1100'))

        self.assertEqual(slot1.compare_with(slot2), WdcTimeSlotComparison.BEFORE)

    def test_after_touching(self):
        slot1 = WdcTimeSlot(start=WdcTime('0800'), end=WdcTime('0900'))
        slot2 = WdcTimeSlot(start=WdcTime('0900'), end=WdcTime('1000'))

        self.assertEqual(slot1.compare_with(slot2), WdcTimeSlotComparison.BEFORE)


class ComparissonOperators(unittest.TestCase):
    def test_slot1_bigger_touching(self):
        slot1 = WdcTimeSlot(start=WdcTime('0800'), end=WdcTime('0900'))
        slot2 = WdcTimeSlot(start=WdcTime('0700'), end=WdcTime('0800'))

        self.assertTrue(slot1 > slot2)

    def test_slot1_smaller_touching(self):
        slot1 = WdcTimeSlot(start=WdcTime('0700'), end=WdcTime('0800'))
        slot2 = WdcTimeSlot(start=WdcTime('0800'), end=WdcTime('0900'))

        self.assertTrue(slot1 < slot2)

    def test_slot1_bigger(self):
        slot1 = WdcTimeSlot(start=WdcTime('0900'), end=WdcTime('1000'))
        slot2 = WdcTimeSlot(start=WdcTime('0700'), end=WdcTime('0800'))

        self.assertTrue(slot1 > slot2)

    def test_slot1_smaller(self):
        slot1 = WdcTimeSlot(start=WdcTime('0600'), end=WdcTime('0700'))
        slot2 = WdcTimeSlot(start=WdcTime('0800'), end=WdcTime('0900'))

        self.assertTrue(slot1 < slot2)
