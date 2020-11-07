import unittest
from unittest.mock import patch

from wdc.classes import WdcTask, WdcTags
from wdc.controller.tasks import list_tasks
from wdc.time import WdcFullDate, WdcTime


class ListWorkTasksFixture(unittest.TestCase):
    def test_invalid_date(self):
        self.assertRaises(ValueError, list_tasks, '9999-99-99')
        self.assertRaises(ValueError, list_tasks, '')

    @patch('wdc.controller.tasks.WdcTaskStore')
    def test_task_are_sorted(self, mock_store):
        mock_store.return_value.get.return_value = [
            WdcTask(
                id='task1',
                date=WdcFullDate('2020-10-25'),
                start=WdcTime('0800'),
                end=WdcTime('0900'),
                tags=WdcTags(['t1']),
                description='test_description1',
                timestamp='22'
            ),
            WdcTask(
                id='task2',
                date=WdcFullDate('2020-10-25'),
                start=WdcTime('0800'),
                end=WdcTime('0900'),
                tags=WdcTags(['t2']),
                description='test_description2',
                timestamp='11'
            )
        ]

        results = list_tasks(WdcFullDate('2020-10-25'))

        self.assertEqual(2, len(results))
        self.assertEqual('task2', results[0].id)
        self.assertEqual('task1', results[1].id)
