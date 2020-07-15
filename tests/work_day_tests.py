import unittest
from unittest.mock import patch
from freezegun import freeze_time
from wdc.controller.work_day import start_work_task

class StartWorkdayTaskFixture(unittest.TestCase):

    @patch('wdc.controller.work_day.append_line')
    def test_all_parameters_given(self, mock_append_line):
        start_work_task('0800', '0815', ['t1', 't2'], 'description', '2020-10-25')

        mock_append_line.assert_called()
        call_args = mock_append_line.call_args.args[0]
        
        self.assertEqual('2020-10-25', call_args[1])
        self.assertEqual('0800', call_args[2])
        self.assertEqual('0815', call_args[3])
        self.assertEqual('t1,t2', call_args[4])
        self.assertEqual('description', call_args[5])

    @patch('wdc.controller.work_day.append_line')
    def test_no_end_time_given(self, mock_append_line):
        start_work_task('0800', None, ['t1', 't2'], 'description', '2020-10-25')

        mock_append_line.assert_called()
        call_args = mock_append_line.call_args.args[0]
        
        self.assertEqual('2020-10-25', call_args[1])
        self.assertEqual('0800', call_args[2])
        self.assertEqual('', call_args[3])
        self.assertEqual('t1,t2', call_args[4])
        self.assertEqual('description', call_args[5])
    
    @patch('wdc.controller.work_day.append_line')
    def test_no_tags_given(self, mock_append_line):
        start_work_task('0800', '0815', [], 'description', '2020-10-25')

        mock_append_line.assert_called()
        call_args = mock_append_line.call_args.args[0]
        
        self.assertEqual('2020-10-25', call_args[1])
        self.assertEqual('0800', call_args[2])
        self.assertEqual('0815', call_args[3])
        self.assertEqual('', call_args[4])
        self.assertEqual('description', call_args[5])

    @patch('wdc.controller.work_day.append_line')
    def test_no_description_given(self, mock_append_line):
        start_work_task('0800', '0815', ['t1', 't2'], None, '2020-10-25')

        mock_append_line.assert_called()
        call_args = mock_append_line.call_args.args[0]
        
        self.assertEqual('2020-10-25', call_args[1])
        self.assertEqual('0800', call_args[2])
        self.assertEqual('0815', call_args[3])
        self.assertEqual('t1,t2', call_args[4])
        self.assertEqual('', call_args[5])

    @freeze_time('2019-10-25')
    @patch('wdc.controller.work_day.append_line')
    def test_no_date_then_today(self, mock_append_line):
        start_work_task('0800', '0815', ['t1', 't2'], 'description', None)

        mock_append_line.assert_called()
        call_args = mock_append_line.call_args.args[0]
        
        self.assertEqual('2019-10-25', call_args[1])
        self.assertEqual('0800', call_args[2])
        self.assertEqual('0815', call_args[3])
        self.assertEqual('t1,t2', call_args[4])
        self.assertEqual('description', call_args[5])