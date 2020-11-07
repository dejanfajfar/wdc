import unittest
from unittest.mock import patch

from wdc.classes import WdcTags, WdcTask
from wdc.controller.tasks import start_work_task
from wdc.time import WdcTime, WdcFullDate


class StartWorkdayTaskFixture(unittest.TestCase):

    def test_only_start_given(self):
        self.assertRaises(ValueError, start_work_task, WdcTime('0800'), None, None, '', None)

    @patch('wdc.controller.tasks.WdcTaskStore')
    def test_all_parameters_given(self, mock_storage):
        start_work_task(WdcTime('0800'), WdcTime('0815'), WdcTags(['t1', 't2']), 'description',
                        WdcFullDate('2020-10-25'))

        mock_storage.return_value.add_and_save.assert_called()
        call_args = mock_storage.return_value.add_and_save.call_args.args[0]

        self.assertEqual('2020-10-25', str(call_args.date))
        self.assertEqual('0800', str(call_args.start))
        self.assertEqual('0815', str(call_args.end))
        self.assertEqual('T1,T2', str(call_args.tags))
        self.assertEqual('description', call_args.description)

    @patch('wdc.controller.tasks.WdcTaskStore')
    def test_no_end_time_given(self, mock_storage):
        start_work_task(WdcTime('0800'), None, WdcTags(['t1', 't2']), 'description',
                        WdcFullDate('2020-10-25'))

        mock_storage.return_value.add_and_save.assert_called()
        call_args = mock_storage.return_value.add_and_save.call_args.args[0]

        self.assertEqual('2020-10-25', str(call_args.date))
        self.assertEqual('0800', str(call_args.start))
        self.assertEqual(None, call_args.end)
        self.assertEqual('T1,T2', str(call_args.tags))
        self.assertEqual('description', call_args.description)

    @patch('wdc.controller.tasks.WdcTaskStore')
    def test_no_tags_given(self, mock_storage):
        start_work_task(WdcTime('0800'), WdcTime('0815'), WdcTags([]), 'description', WdcFullDate('2020-10-25'))

        mock_storage.return_value.add_and_save.assert_called()
        call_args = mock_storage.return_value.add_and_save.call_args.args[0]

        self.assertEqual('2020-10-25', str(call_args.date))
        self.assertEqual('0800', str(call_args.start))
        self.assertEqual('0815', str(call_args.end))
        self.assertEqual('', str(call_args.tags))
        self.assertEqual('description', call_args.description)

    @patch('wdc.controller.tasks.WdcTaskStore')
    def test_no_description_given(self, mock_storage):
        start_work_task(WdcTime('0800'), WdcTime('0815'), WdcTags(['t1', 't2']), '', WdcFullDate('2020-10-25'))

        mock_storage.return_value.add_and_save.assert_called()
        call_args = mock_storage.return_value.add_and_save.call_args.args[0]

        self.assertEqual('2020-10-25', str(call_args.date))
        self.assertEqual('0800', str(call_args.start))
        self.assertEqual('0815', str(call_args.end))
        self.assertEqual('T1,T2', str(call_args.tags))
        self.assertEqual('', call_args.description)

    @patch('wdc.controller.tasks.WdcTaskStore')
    def test_set_end_time_of_predecessor(self, mock_storage):
        mock_storage.return_value.get.return_value = [WdcTask(
            id='c411c941',
            date=WdcFullDate('2020-10-25'),
            start=WdcTime('1000'),
            end=None,
            tags=WdcTags(['home']),
            description='test description',
            timestamp='1595423306302'
        )]

        start_work_task(WdcTime('1100'), WdcTime('1200'), WdcTags(['t1', 't2']), '', WdcFullDate('2020-10-25'))

        mock_storage.return_value.add.assert_called()
        mock_storage.return_value.save.assert_called()
        call_args = mock_storage.return_value.add.mock_calls[0].args[0]

        self.assertEqual('2020-10-25', str(call_args.date))
        self.assertEqual('1000', str(call_args.start))
        self.assertEqual('1100', str(call_args.end))
        self.assertEqual('HOME', str(call_args.tags))
        self.assertEqual('test description', call_args.description)

    def test_no_date(self):
        self.assertRaises(ValueError, start_work_task, WdcTime('0800'), WdcTime('0815'), WdcTags(['t1', 't2']),
                          'description', None)

    def test_invalid_start_time(self):
        self.assertRaises(ValueError, start_work_task, '9999', '', [], '', '')

    def test_invalid_end_time(self):
        self.assertRaises(ValueError, start_work_task, '0800', '9999', [], '', '')

    def test_invalid_date(self):
        self.assertRaises(ValueError, start_work_task, '0800', '', [], '', '9999-99-99')
