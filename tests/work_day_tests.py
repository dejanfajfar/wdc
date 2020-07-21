import unittest
from unittest.mock import patch
from freezegun import freeze_time
from wdc.controller.work_day import start_work_task, list_tasks
from wdc.helper.io import WdcTask


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


class ListWorkTasksFixture(unittest.TestCase):
    def test_invalid_date(self):
        self.assertRaises(ValueError, list_tasks, '9999-99-99', False)

    @patch('wdc.controller.work_day.read_all_tasks')
    def test_return_tasks_for_given_day(self, mock_reader):
        mock_reader.return_value = [
            WdcTask(
                id='task1',
                date='2020-10-25',
                start='0800',
                end='0900',
                tags='t1',
                description='test_description1',
                timestamp='11'
            ),
            WdcTask(
                id='task2',
                date='2020-10-26',
                start='0800',
                end='0900',
                tags='t2',
                description='test_description2',
                timestamp='22'
            )
        ]

        results = list_tasks('2020-10-25', True)

        self.assertEqual(1, len(results))
        self.assertEqual('task1', results[0].id)

    @patch('wdc.controller.work_day.read_all_tasks')
    def test_task_are_sorted(self, mock_reader):
        mock_reader.return_value = [
            WdcTask(
                id='task1',
                date='2020-10-25',
                start='0800',
                end='0900',
                tags='t1',
                description='test_description1',
                timestamp='22'
            ),
            WdcTask(
                id='task2',
                date='2020-10-25',
                start='0800',
                end='0900',
                tags='t2',
                description='test_description2',
                timestamp='11'
            )
        ]

        results = list_tasks('2020-10-25', True)

        self.assertEqual(2, len(results))
        self.assertEqual('task2', results[0].id)
        self.assertEqual('task1', results[1].id)

    @patch('wdc.controller.work_day.read_all_tasks')
    def test_filter_duplicate_tasks(self, mock_reader):
        mock_reader.return_value = [
            WdcTask(
                id='task',
                date='2020-10-25',
                start='0800',
                end='0900',
                tags='t1',
                description='test_description1',
                timestamp='11'
            ),
            WdcTask(
                id='task',
                date='2020-10-25',
                start='0800',
                end='1000',
                tags='t1',
                description='test_description1',
                timestamp='22'
            )
        ]

        results = list_tasks('2020-10-25', False)

        self.assertEqual(1, len(results))
        self.assertEqual('1000', results[0].end)

    @patch('wdc.controller.work_day.read_all_tasks')
    def test_filter_duplicate_tasks_still_solrted(self, mock_reader):
        mock_reader.return_value = [
            WdcTask(
                id='task',
                date='2020-10-25',
                start='0800',
                end='0900',
                tags='t1',
                description='test_description1',
                timestamp='11'
            ),
            WdcTask(
                id='task',
                date='2020-10-25',
                start='0800',
                end='1000',
                tags='t1',
                description='test_description1',
                timestamp='22'
            ),
            WdcTask(
                id='task2',
                date='2020-10-25',
                start='10000',
                end='1130',
                tags='t2',
                description='test_description1',
                timestamp='33'
            )
        ]

        results = list_tasks('2020-10-25', False)

        self.assertEqual(2, len(results))
        self.assertEqual('1000', results[0].end)
        self.assertEqual('task', results[0].id)
        self.assertEqual('22', results[0].timestamp)
        self.assertEqual('task2', results[1].id)
        self.assertEqual('33', results[1].timestamp)
