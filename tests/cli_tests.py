import unittest
from unittest.mock import patch

from click.testing import CliRunner
from freezegun import freeze_time

from wdc.analytics.task_analyser import analyse_tasks
from wdc.classes import WdcTask
from wdc.controller.export_import import ExportType
from wdc.runner import cli, task_to_printout, print_info, print_week_stats


class CalcCommandFixture(unittest.TestCase):
    def setUp(self):
        self.cli_runner = CliRunner()

    def test_valid_no_options(self):
        result = self.cli_runner.invoke(cli, ['calc', '0800'])
        self.assertEqual(0, result.exit_code)
        self.assertIn('1615', result.output)

    def test_valid_given_break(self):
        with self.subTest('short option name'):
            result = self.cli_runner.invoke(cli, ['calc', '0800', '-b', 45])
            self.assertIn('1630', result.output)

        with self.subTest('long option name'):
            result = self.cli_runner.invoke(cli, ['calc', '0800', '--break_duration', 45])
            self.assertIn('1630', result.output)

    def test_valid_given_workday_duration(self):
        result = self.cli_runner.invoke(cli, ['calc', '0800', '-d', '0800'])
        self.assertIn('1630', result.output)

        result = self.cli_runner.invoke(cli, ['calc', '0800', '-d', '0800'])
        self.assertIn('1630', result.output)

    def test_invalid_start_time_no_options(self):
        result = self.cli_runner.invoke(cli, ['calc', '0860'])
        self.assertEqual(2, result.exit_code)
        self.assertIn('Error: Invalid value for \'WORKDAY_START\': 0860 is not a valid time', result.output)

    def test_invalid_workday_duration(self):
        result = self.cli_runner.invoke(cli, ['calc', '0800', '-d', '0860'])
        self.assertIn('0860 is not a valid time', result.output)


class StartWorkTaskFixture(unittest.TestCase):
    def setUp(self):
        self.cli_runner = CliRunner()

    @patch('wdc.runner.start_work_task')
    def test_valid_all_options(self, mock_controller):
        self.cli_runner.invoke(cli, ['start', '0800', '-t', 't1', '-t', 't2', '-e',
                                     '0900', '-m', 'description', '-d', '2020-10-25'])
        mock_controller.assert_called()

        call_args = mock_controller.call_args.args

        self.assertEqual('0800', call_args[0])
        self.assertEqual('0900', call_args[1])
        self.assertEqual(['t1', 't2'], call_args[2])
        self.assertEqual('description', call_args[3])
        self.assertEqual('2020-10-25', call_args[4])

    @patch('wdc.runner.start_work_task')
    def test_valid_all_options_long(self, mock_controller):
        self.cli_runner.invoke(cli, ['start', '0800', '--tag', 't1', '--tag', 't2', '--end',
                                     '0900', '--message', 'description', '--date', '2020-10-25'])
        mock_controller.assert_called()

        call_args = mock_controller.call_args.args

        self.assertEqual('0800', call_args[0])
        self.assertEqual('0900', call_args[1])
        self.assertEqual(['t1', 't2'], call_args[2])
        self.assertEqual('description', call_args[3])
        self.assertEqual('2020-10-25', call_args[4])

    @unittest.skip('Experimentation integration test')
    def test_go(self):
        self.cli_runner.invoke(cli, ['start', '0800', '--tag', 't1', '--tag', 't2', '--message', 'description'])
        self.cli_runner.invoke(cli, ['start', '1000', '--tag', 't1', '--tag', 't2', '--end',
                                     '1100', '--message', 'description'])

        result = self.cli_runner.invoke(cli, ['list'])
        print(result.output)

        result = self.cli_runner.invoke(cli, ['--help'])
        print(result.output)

    @freeze_time('2020-07-25')
    @patch('wdc.runner.start_work_task')
    def test_valid_only_start(self, mock_controller):
        self.cli_runner.invoke(cli, ['start', '0800'])
        mock_controller.assert_called()

        call_args = mock_controller.call_args.args

        self.assertEqual('0800', call_args[0])
        self.assertEqual('', call_args[1])
        self.assertEqual([], call_args[2])
        self.assertEqual('', call_args[3])
        self.assertEqual('2020-07-25', call_args[4])

    @patch('wdc.runner.start_work_task')
    def test_invalid_start_time(self, mock_controller):
        result = self.cli_runner.invoke(cli, ['start', '9999'])
        self.assertIn('9999', result.output)
        mock_controller.assert_not_called()


class ListWorkTasksFixture(unittest.TestCase):
    def setUp(self):
        self.cli_runner = CliRunner()

    @patch('wdc.runner.list_tasks')
    def test_valid(self, mock_controller):
        mock_controller.return_value = [
            WdcTask(
                id='test_id',
                date='2020-10-25',
                start='0800',
                end='0900',
                tags='t1',
                description='test_description',
                timestamp='11'
            )
        ]

        result = self.cli_runner.invoke(cli, ['list'])

        self.assertIn('│ test_id │ 2020-10-25 │ 08:00 │ 09:00 │ t1   │ test_descr.. │', result.output)

    @patch('wdc.runner.list_tasks')
    def test_minimal_task_valid(self, mock_controller):
        mock_controller.return_value = [
            WdcTask(
                id='test_id',
                date='2020-10-25',
                start='0800',
                end='',
                tags='',
                description='',
                timestamp='11'
            )
        ]

        result = self.cli_runner.invoke(cli, ['list'])

        self.assertIn('│ test_id │ 2020-10-25 │ 08:00 │     │      │             │', result.output)

    @patch('wdc.runner.list_tasks')
    def test_no_tasks_found(self, mock_controller):
        mock_controller.return_value = []

        result = self.cli_runner.invoke(cli, ['list'])

        self.assertIn('No tasks found', result.output)


class HelperFunctionsFixture(unittest.TestCase):
    def test_task_to_printout_valid(self):
        test_object = WdcTask(
            id='testId',
            date='2020-10-25',
            start='0800',
            end='0900',
            tags='t1',
            description='testDescription',
            timestamp='11'
        )

        result = task_to_printout(test_object)

        self.assertSequenceEqual(result, ['testId', '2020-10-25', '08:00', '09:00', 't1', 'testDescri..'])


class AmendTaskFixture(unittest.TestCase):
    def setUp(self):
        self.cli_runner = CliRunner()

    @patch('wdc.runner.amend_task')
    def test_all_parameters_given(self, mock_controller):
        self.cli_runner.invoke(cli, ['amend', 'id1', '-s', '0800', '-e',
                                              '0900', '-t', 't1', '-m', 'test message', '-d', '2020-10-25'])

        mock_controller.assert_called()

        self.assertEqual('id1', mock_controller.call_args.args[0])
        self.assertEqual('0800', mock_controller.call_args.kwargs['start'])
        self.assertEqual('0900', mock_controller.call_args.kwargs['end'])
        self.assertEqual(['t1'], mock_controller.call_args.kwargs['tags'])
        self.assertEqual('test message', mock_controller.call_args.kwargs['message'])
        self.assertEqual('2020-10-25', mock_controller.call_args.kwargs['date'])

    @patch('wdc.runner.amend_task')
    def test_no_parameters_given(self, mock_controller):
        self.cli_runner.invoke(cli, ['amend', 'id1'])

        mock_controller.assert_called()

        self.assertEqual('id1', mock_controller.call_args.args[0])
        self.assertEqual('', mock_controller.call_args.kwargs['start'])
        self.assertEqual('', mock_controller.call_args.kwargs['end'])
        self.assertEqual([], mock_controller.call_args.kwargs['tags'])
        self.assertEqual('', mock_controller.call_args.kwargs['message'])
        self.assertEqual('', mock_controller.call_args.kwargs['date'])

    @patch('wdc.runner.amend_task')
    def test_handle_valueError(self, mock_controller):
        mock_controller.side_effect = ValueError('')

        result = self.cli_runner.invoke(cli, ['amend', 'id'])

        self.assertIn('!!', result.output)


class ExportCommandFixture(unittest.TestCase):
    """
    Fixture for the EXPORT command of wdc

    All unit tests regarding to the export command are located inside this class/fixture
    """

    def setUp(self):
        self.cli_runner = CliRunner()

    @patch('wdc.runner.export_tasks')
    def test_no_options(self, mock_controller):
        result = self.cli_runner.invoke(cli, ['export'])

        self.assertEqual(0, result.exit_code)

        call_args = mock_controller.call_args.kwargs

        # Assert that no date to export is given
        self.assertEqual('', call_args['date'])
        # Assert that no output for the export is given
        self.assertEqual('', call_args['file_path'])
        # Assert that JSON is selected as the export type
        self.assertEqual(ExportType.JSON, call_args['export_to'])
        # Assert that only the latest task version are requested
        self.assertFalse(call_args['export_all'])

    @patch('wdc.runner.export_tasks')
    def test_all_options_given(self, mock_controller):
        result = self.cli_runner.invoke(cli,
                                        ['export', '-d', '2020-10-25', '-o', 'export_today.csv', '--csv', '--raw'])

        self.assertEqual(0, result.exit_code)

        call_args = mock_controller.call_args.kwargs

        # Assert that no date to export is given
        self.assertEqual('2020-10-25', call_args['date'])
        # Assert that no output for the export is given
        self.assertEqual('export_today.csv', call_args['file_path'])
        # Assert that JSON is selected as the export type
        self.assertEqual(ExportType.CSV, call_args['export_to'])
        # Assert that the RAW flag is set to true
        self.assertTrue(call_args['export_all'])


class PrintHelperFixture(unittest.TestCase):
    """
    Unit tests for all the print testing functions in the application
    """

    @patch('builtins.print')
    def test_info(self, mock_print):
        print_info('Test message')

        mock_print.assert_called_with('\n\x1b[38;5;0m\x1b[48;5;164minfo: Test message \x1b[0m\n')


class PrintWeekStats(unittest.TestCase):
    def setUp(self) -> None:
        self.analysis_data = analyse_tasks([
            WdcTask('0001', '2020-10-19', '0800', '1015', 'CUST1,task1', ''),
            WdcTask('0001', '2020-10-19', '1015', '1030', 'CUST1,BESPR', ''),
            WdcTask('0001', '2020-10-19', '1130', '1200', 'LUNCH', ''),
            WdcTask('0001', '2020-10-19', '1200', '1600', 'CUST1,task1', ''),
            WdcTask('0001', '2020-10-19', '1600', '1700', 'CUST1,tag1,tag2', ''),
            WdcTask('0001', '2020-10-20', '0800', '0900', 'CUST1,task3', ''),
            WdcTask('0001', '2020-10-20', '0900', '1015', 'CUST1,task1', ''),
            WdcTask('0001', '2020-10-20', '1015', '1030', 'CUST1,BESPR', ''),
            WdcTask('0001', '2020-10-20', '1130', '1200', 'LUNCH', ''),
            WdcTask('0001', '2020-10-20', '1200', '1600', 'CUST1,task1', ''),
            WdcTask('0001', '2020-10-20', '1600', '1700', 'CUST1,tag1,tag2', ''),
            WdcTask('0001', '2020-10-21', '1000', '1200', 'CUST2', ''),
            WdcTask('0001', '2020-10-21', '1200', '1500', 'CUST1,task1', ''),
        ])

    def test_print(self):
        print_week_stats(self.analysis_data, 43)
