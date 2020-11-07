import unittest

from wdc.classes import WdcTask, WdcTags
from wdc.controller.tasks import sort_by_time
from wdc.time import WdcFullDate, WdcTime


class SortTasksByTimeFixture(unittest.TestCase):
    def test_valid_ascending(self):
        test_object = [WdcTask(
            id='1',
            date=WdcFullDate('2020-10-25'),
            start=WdcTime('0800'),
            end=WdcTime('0900'),
            tags=WdcTags(['t1']),
            description='description',
            timestamp='11'
        ),
            WdcTask(
                id='2',
                date=WdcFullDate('2020-10-25'),
                start=WdcTime('1000'),
                end=WdcTime('1100'),
                tags=WdcTags(['t1']),
                description='description',
                timestamp='2'
        ),
            WdcTask(
                id='3',
                date=WdcFullDate('2020-10-25'),
                start=WdcTime('0900'),
                end=WdcTime('1000'),
                tags=WdcTags(['t1']),
                description='description',
                timestamp='33'
        )]

        result = sort_by_time(test_object)

        self.assertEqual('1', result[0].id)
        self.assertEqual('3', result[1].id)
        self.assertEqual('2', result[2].id)

    def test_valid_descending(self):
        test_object = [WdcTask(
            id='1',
            date=WdcFullDate('2020-10-25'),
            start=WdcTime('0800'),
            end=WdcTime('0900'),
            tags=WdcTags(['t1']),
            description='description',
            timestamp='11'
        ),
            WdcTask(
                id='2',
                date=WdcFullDate('2020-10-25'),
                start=WdcTime('1000'),
                end=WdcTime('1100'),
                tags=WdcTags(['t1']),
                description='description',
                timestamp='2'
        ),
            WdcTask(
                id='3',
                date=WdcFullDate('2020-10-25'),
                start=WdcTime('0900'),
                end=WdcTime('1000'),
                tags=WdcTags(['t1']),
                description='description',
                timestamp='33'
        )]

        result = sort_by_time(test_object, descending=True)

        self.assertEqual('2', result[0].id)
        self.assertEqual('3', result[1].id)
        self.assertEqual('1', result[2].id)
