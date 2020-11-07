import unittest
from unittest.mock import patch

from wdc.classes import WdcTask, WdcTags
from wdc.controller.tasks import amend_task
from wdc.time import WdcFullDate, WdcTime


class AmendTaskFixture(unittest.TestCase):

    @patch('wdc.controller.tasks.WdcTaskStore')
    @patch('wdc.controller.tasks.find_stores')
    def test_replace_all(self, mock_finder, mock_store):
        mock_store.return_value.get.return_value = [
            WdcTask(
                id='c411c941',
                date=WdcFullDate('2020-10-25'),
                start=WdcTime('0930'),
                end=WdcTime('1000'),
                tags=WdcTags(['home']),
                description='test description',
                timestamp='1595423306302'
            )
        ]
        mock_finder.return_value = [mock_store.return_value]

        amend_task('c411c941',
                   tags=WdcTags(['t1', 't2']),
                   start=WdcTime('1000'),
                   end=WdcTime('1130'),
                   message='test message',
                   date=WdcFullDate('2020-08-18'))

        call_args = mock_store.return_value.add_and_save.call_args.args[0]

        self.assertEqual('c411c941', call_args.id)
        self.assertEqual('T1,T2', call_args.tags)
        self.assertEqual('1000', str(call_args.start))
        self.assertEqual('1130', str(call_args.end))
        self.assertEqual('test message', call_args.description)
        self.assertEqual('2020-08-18', str(call_args.date))

    @patch('wdc.controller.tasks.WdcTaskStore')
    @patch('wdc.controller.tasks.find_stores')
    def test_none_replaced(self, mock_finder, mock_store):
        mock_store.return_value.get.return_value = [
            WdcTask(
                id='c411c941',
                date=WdcFullDate('2020-10-25'),
                start=WdcTime('0930'),
                end=WdcTime('1000'),
                tags=WdcTags(['home']),
                description='test description',
                timestamp='1595423306302'
            )
        ]
        mock_finder.return_value = [mock_store.return_value]

        amend_task('c411c941', tags=WdcTags([]), start=None, end=None, message='', date=None)

        call_args = mock_store.return_value.add_and_save.call_args.args[0]

        self.assertEqual('c411c941', call_args.id)
        self.assertEqual('HOME', str(call_args.tags))
        self.assertEqual('0930', str(call_args.start))
        self.assertEqual('1000', str(call_args.end))
        self.assertEqual('2020-10-25', str(call_args.date))
        self.assertEqual('test description', call_args.description)

    def test_invalid_start_time(self):
        self.assertRaises(ValueError, amend_task, 'c411c941', [], '9999', '', '', '')

    def test_invalid_end_time(self):
        self.assertRaises(ValueError, amend_task, 'c411c941', [], '', '9999', '', '')

    def test_invalid_date(self):
        self.assertRaises(ValueError, amend_task, 'c411c941', [], '', '', '', '9999-99-99')
