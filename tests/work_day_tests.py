import unittest
from unittest.mock import patch
from freezegun import freeze_time
from wdc.controller.work_day import start_work_task


class StartWorkdayTaskFixture(unittest.TestCase):

    @freeze_time('2019-10-25')
    @patch('wdc.controller.work_day.write_task')
    def test_only_start_given(self, mock_write_line):
        start_work_task('0800', '', (), '', '')

        mock_write_line.assert_called()
        call_args = mock_write_line.call_args.args[0]

        self.assertEqual('2019-10-25', call_args.date)
        self.assertEqual('0800', call_args.start)
        self.assertEqual('', call_args.end)
        self.assertEqual('', call_args.tags)
        self.assertEqual('', call_args.description)

    @patch('wdc.controller.work_day.write_task')
    def test_all_parameters_given(self, mock_append_line):
        start_work_task('0800', '0815', ('t1', 't2'), 'description', '2020-10-25')

        mock_append_line.assert_called()
        call_args = mock_append_line.call_args.args[0]

        self.assertEqual('2020-10-25', call_args.date)
        self.assertEqual('0800', call_args.start)
        self.assertEqual('0815', call_args.end)
        self.assertEqual('t1,t2', call_args.tags)
        self.assertEqual('description', call_args.description)

    @patch('wdc.controller.work_day.write_task')
    def test_no_end_time_given(self, mock_append_line):
        start_work_task('0800', '', ('t1', 't2'), 'description', '2020-10-25')

        mock_append_line.assert_called()
        call_args = mock_append_line.call_args.args[0]

        self.assertEqual('2020-10-25', call_args.date)
        self.assertEqual('0800', call_args.start)
        self.assertEqual('', call_args.end)
        self.assertEqual('t1,t2', call_args.tags)
        self.assertEqual('description', call_args.description)

    @patch('wdc.controller.work_day.write_task')
    def test_no_tags_given(self, mock_append_line):
        start_work_task('0800', '0815', (), 'description', '2020-10-25')

        mock_append_line.assert_called()
        call_args = mock_append_line.call_args.args[0]

        self.assertEqual('2020-10-25', call_args.date)
        self.assertEqual('0800', call_args.start)
        self.assertEqual('0815', call_args.end)
        self.assertEqual('', call_args.tags)
        self.assertEqual('description', call_args.description)

    @patch('wdc.controller.work_day.write_task')
    def test_no_description_given(self, mock_append_line):
        start_work_task('0800', '0815', ('t1', 't2'), '', '2020-10-25')

        mock_append_line.assert_called()
        call_args = mock_append_line.call_args.args[0]

        self.assertEqual('2020-10-25', call_args.date)
        self.assertEqual('0800', call_args.start)
        self.assertEqual('0815', call_args.end)
        self.assertEqual('t1,t2', call_args.tags)
        self.assertEqual('', call_args.description)

    @freeze_time('2019-10-25')
    @patch('wdc.controller.work_day.write_task')
    def test_no_date_then_today(self, mock_append_line):
        start_work_task('0800', '0815', ('t1', 't2'), 'description', '')

        mock_append_line.assert_called()
        call_args = mock_append_line.call_args.args[0]

        self.assertEqual('2019-10-25', call_args.date)
        self.assertEqual('0800', call_args.start)
        self.assertEqual('0815', call_args.end)
        self.assertEqual('t1,t2', call_args.tags)
        self.assertEqual('description', call_args.description)

    def test_invalid_start_time(self):
        self.assertRaises(ValueError, start_work_task, '9999', '', (), '', '')

    def test_invalid_end_time(self):
        self.assertRaises(ValueError, start_work_task, '0800', '9999', (), '', '')

    def test_invalid_date(self):
        self.assertRaises(ValueError, start_work_task, '0800', '', (), '', '9999-99-99')
