import unittest
from unittest.mock import patch

from wdc.classes import WdcTask
from wdc.persistence.task_store import WdcTaskStore


class SaveTasksFixture(unittest.TestCase):
    @patch('wdc.persistence.task_store.read_all_tasks')
    @patch('wdc.persistence.task_store.write_tasks')
    def test_sort_all_ok(self, mock_writer, mock_reader):
        mock_reader.return_value = [
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
                start='0830',
                end='1000',
                tags='home',
                description='test description',
                timestamp='1595423306302'
            )
        ]

        store = WdcTaskStore('2020-10-25')
        store.save()

        mock_writer.assert_called()
