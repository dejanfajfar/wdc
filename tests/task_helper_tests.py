import unittest

from wdc.classes import WdcTask, WdcTags
from wdc.helper.taks import overlaps
from wdc.time import WdcFullDate, WdcTime


class Overlaps(unittest.TestCase):
    def test_empty_list(self):
        test_task = WdcTask(
            id='c411c941',
            date=WdcFullDate('2020-10-25'),
            start=WdcTime('1000'),
            end=WdcTime('1130'),
            tags=WdcTags(['home']),
            description='test description',
            timestamp='1595423306302'
        )

        self.assertFalse(overlaps(test_task, []))

    def test_no_tasks_for_same_day(self):
        test_task = WdcTask(
            id='c411c941',
            date=WdcFullDate('2020-10-25'),
            start=WdcTime('1000'),
            end=WdcTime('1130'),
            tags=WdcTags(['home']),
            description='test description',
            timestamp='1595423306302'
        )

        test_tasks = [
            WdcTask(
                id='c411c941',
                date=WdcFullDate('2020-10-26'),
                start=WdcTime('1000'),
                end=WdcTime('1130'),
                tags=WdcTags(['home']),
                description='test description',
                timestamp='1595423306302'
            ),
            WdcTask(
                id='c411c941',
                date=WdcFullDate('2020-10-27'),
                start=WdcTime('1130'),
                end=WdcTime('1200'),
                tags=WdcTags(['home']),
                description='test description',
                timestamp='1595423306302'
            )
        ]

        self.assertFalse(overlaps(test_task, test_tasks))

    def test_task_after_end_of_day(self):
        test_task = WdcTask(
            id='c411c941',
            date=WdcFullDate('2020-10-25'),
            start=WdcTime('1200'),
            end=WdcTime('1230'),
            tags=WdcTags(['home']),
            description='test description',
            timestamp='1595423306302'
        )

        test_tasks = [
            WdcTask(
                id='c411c941',
                date=WdcFullDate('2020-10-25'),
                start=WdcTime('1000'),
                end=WdcTime('1130'),
                tags=WdcTags(['home']),
                description='test description',
                timestamp='1595423306302'
            ),
            WdcTask(
                id='c411c941',
                date=WdcFullDate('2020-10-25'),
                start=WdcTime('1130'),
                end=WdcTime('1200'),
                tags=WdcTags(['home']),
                description='test description',
                timestamp='1595423306302'
            )
        ]

        self.assertFalse(overlaps(test_task, test_tasks))

    def test_task_before_start_of_day(self):
        test_task = WdcTask(
            id='c411c941',
            date=WdcFullDate('2020-10-25'),
            start=WdcTime('0900'),
            end=WdcTime('1000'),
            tags=WdcTags(['home']),
            description='test description',
            timestamp='1595423306302'
        )

        test_tasks = [
            WdcTask(
                id='c411c941',
                date=WdcFullDate('2020-10-25'),
                start=WdcTime('1000'),
                end=WdcTime('1130'),
                tags=WdcTags(['home']),
                description='test description',
                timestamp='1595423306302'
            ),
            WdcTask(
                id='c411c941',
                date=WdcFullDate('2020-10-25'),
                start=WdcTime('1130'),
                end=WdcTime('1200'),
                tags=WdcTags(['home']),
                description='test description',
                timestamp='1595423306302'
            )
        ]

        self.assertFalse(overlaps(test_task, test_tasks))

    def test_ongoing_task_before(self):
        test_task = WdcTask(
            id='c411c941',
            date=WdcFullDate('2020-10-25'),
            start=WdcTime('1200'),
            end=None,
            tags=WdcTags(['home']),
            description='test description',
            timestamp='1595423306302'
        )

        test_tasks = [
            WdcTask(
                id='c411c941',
                date=WdcFullDate('2020-10-25'),
                start=WdcTime('1000'),
                end=WdcTime('1130'),
                tags=WdcTags(['home']),
                description='test description',
                timestamp='1595423306302'
            ),
            WdcTask(
                id='c411c941',
                date=WdcFullDate('2020-10-25'),
                start=WdcTime('1130'),
                end=None,
                tags=WdcTags(['home']),
                description='test description',
                timestamp='1595423306302'
            )
        ]

        self.assertFalse(overlaps(test_task, test_tasks))
