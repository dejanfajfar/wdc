import unittest
from unittest.mock import patch

from wdc.classes import WdcTask, WdcTags
from wdc.persistence.task_store import WdcTaskStore
from wdc.time import WdcFullDate, WdcTime


class SaveTasksFixture(unittest.TestCase):
    @patch('wdc.persistence.task_store.read_all_tasks')
    @patch('wdc.persistence.task_store.write_tasks')
    def test_sort_all_ok(self, mock_writer, mock_reader):
        # TODO: Make an actual unit test
        mock_reader.return_value = [
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
                start=WdcTime('0830'),
                end=WdcTime('1000'),
                tags=WdcTags(['home']),
                description='test description',
                timestamp='1595423306302'
            )
        ]

        store = WdcTaskStore(WdcFullDate('2020-10-25').to_moth_date())
        store.save()

        mock_writer.assert_called()
