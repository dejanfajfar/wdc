import unittest

from wdc.classes import WdcTask
from wdc.helper.taks import overlaps, predecessor


class Overlaps(unittest.TestCase):
    def test_empty_list(self):
        test_task = WdcTask(
            id='c411c941',
            date='2020-10-25',
            start='1000',
            end='1130',
            tags='home',
            description='test description',
            timestamp='1595423306302'
        )

        self.assertFalse(overlaps(test_task, []))

    def test_no_tasks_for_same_day(self):
        test_task = WdcTask(
            id='c411c941',
            date='2020-10-25',
            start='1000',
            end='1130',
            tags='home',
            description='test description',
            timestamp='1595423306302'
        )

        test_tasks = [
            WdcTask(
                id='c411c941',
                date='2020-10-26',
                start='1000',
                end='1130',
                tags='home',
                description='test description',
                timestamp='1595423306302'
            ),
            WdcTask(
                id='c411c941',
                date='2020-10-27',
                start='1130',
                end='1200',
                tags='home',
                description='test description',
                timestamp='1595423306302'
            )
        ]

        self.assertFalse(overlaps(test_task, test_tasks))

    def test_task_after_end_of_day(self):
        test_task = WdcTask(
            id='c411c941',
            date='2020-10-25',
            start='1200',
            end='1230',
            tags='home',
            description='test description',
            timestamp='1595423306302'
        )

        test_tasks = [
            WdcTask(
                id='c411c941',
                date='2020-10-25',
                start='1000',
                end='1130',
                tags='home',
                description='test description',
                timestamp='1595423306302'
            ),
            WdcTask(
                id='c411c941',
                date='2020-10-25',
                start='1130',
                end='1200',
                tags='home',
                description='test description',
                timestamp='1595423306302'
            )
        ]

        self.assertFalse(overlaps(test_task, test_tasks))

    def test_task_before_start_of_day(self):
        test_task = WdcTask(
            id='c411c941',
            date='2020-10-25',
            start='0900',
            end='1000',
            tags='home',
            description='test description',
            timestamp='1595423306302'
        )

        test_tasks = [
            WdcTask(
                id='c411c941',
                date='2020-10-25',
                start='1000',
                end='1130',
                tags='home',
                description='test description',
                timestamp='1595423306302'
            ),
            WdcTask(
                id='c411c941',
                date='2020-10-25',
                start='1130',
                end='1200',
                tags='home',
                description='test description',
                timestamp='1595423306302'
            )
        ]

        self.assertFalse(overlaps(test_task, test_tasks))


class Predecessor(unittest.TestCase):
    def test_intermediate_task(self):
        test_task = WdcTask(
            id='00T',
            date='2020-10-25',
            start='1030',
            end='1130',
            tags='home',
            description='test description',
            timestamp='1595423306302'
        )

        test_tasks = [
            WdcTask(
                id='001',
                date='2020-10-26',
                start='1000',
                end='1100',
                tags='home',
                description='test description',
                timestamp='1595423306302'
            ),
            WdcTask(
                id='002',
                date='2020-10-27',
                start='1100',
                end='1200',
                tags='home',
                description='test description',
                timestamp='1595423306302'
            ),
            WdcTask(
                id='003',
                date='2020-10-27',
                start='1200',
                end='1300',
                tags='home',
                description='test description',
                timestamp='1595423306302'
            )
        ]

        test_result = predecessor(test_task, test_tasks)
        self.assertIsNone(test_result)

    def test_same_as_last_task(self):
        test_task = WdcTask(
            id='00T',
            date='2020-10-25',
            start='1200',
            end='1300',
            tags='home',
            description='test description',
            timestamp='1595423306302'
        )

        test_tasks = [
            WdcTask(
                id='001',
                date='2020-10-26',
                start='1000',
                end='1100',
                tags='home',
                description='test description',
                timestamp='1595423306302'
            ),
            WdcTask(
                id='002',
                date='2020-10-27',
                start='1100',
                end='1200',
                tags='home',
                description='test description',
                timestamp='1595423306302'
            ),
            WdcTask(
                id='003',
                date='2020-10-27',
                start='1200',
                end='1300',
                tags='home',
                description='test description',
                timestamp='1595423306302'
            )
        ]

        test_result = predecessor(test_task, test_tasks)
        self.assertIsNotNone(test_result)
        self.assertEqual('002', test_result.id)

    def test_no_predecessor(self):
        test_task = WdcTask(
            id='00T',
            date='2020-10-25',
            start='0800',
            end='1300',
            tags='home',
            description='test description',
            timestamp='1595423306302'
        )

        test_tasks = [
            WdcTask(
                id='001',
                date='2020-10-26',
                start='1000',
                end='1100',
                tags='home',
                description='test description',
                timestamp='1595423306302'
            )
        ]

        test_result = predecessor(test_task, test_tasks)
        self.assertIsNone(test_result)

    def test_no_predecessor_option2(self):
        test_task = WdcTask(
            id='00T',
            date='2020-10-25',
            start='0800',
            end='',
            tags='home',
            description='test description',
            timestamp='1595423306302'
        )

        test_tasks = [
            WdcTask(
                id='001',
                date='2020-10-26',
                start='0800',
                end='',
                tags='home',
                description='test description',
                timestamp='1595423306302'
            )
        ]

        test_result = predecessor(test_task, test_tasks)
        self.assertIsNone(test_result)
