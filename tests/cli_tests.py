import unittest
from unittest.mock import patch

from click.testing import CliRunner
from freezegun import freeze_time

from wdc.analytics.task_analyser import analyse_tasks
from wdc.classes import WdcTask, WdcTags
from wdc.controller.export_import import ExportType
from wdc.runner import cli, task_to_printout, print_info, print_statistics
from wdc.time import WdcFullDate, WdcTime, WdcMonthDate


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
        self.assertIn('Time "0860" is not between "0" and "2359"', result.output)

    def test_invalid_workday_duration(self):
        result = self.cli_runner.invoke(cli, ['calc', '0800', '-d', '0860'])
        self.assertIn('Time "0860" is not between "0" and "2359"', result.output)


class StartWorkTaskFixture(unittest.TestCase):
    def setUp(self):
        self.cli_runner = CliRunner()

    @patch('wdc.runner.start_work_task')
    def test_valid_all_options(self, mock_controller):
        self.cli_runner.invoke(cli, ['start', '0800', '-t', 't1', '-t', 't2', '-e',
                                     '0900', '-m', 'description', '-d', '2020-10-25'])
        mock_controller.assert_called()

        call_args = mock_controller.call_args.args

        self.assertEqual('0800', str(call_args[0]))
        self.assertEqual('0900', str(call_args[1]))
        self.assertEqual('T1,T2', str(call_args[2]))
        self.assertEqual('description', call_args[3])
        self.assertEqual('2020-10-25', str(call_args[4]))

    @patch('wdc.runner.start_work_task')
    def test_valid_all_options_long(self, mock_controller):
        self.cli_runner.invoke(cli, ['start', '0800', '--tag', 't1', '--tag', 't2', '--end',
                                     '0900', '--message', 'description', '--date', '2020-10-25'])
        mock_controller.assert_called()

        call_args = mock_controller.call_args.args

        self.assertEqual('0800', str(call_args[0]))
        self.assertEqual('0900', str(call_args[1]))
        self.assertEqual('T1,T2', str(call_args[2]))
        self.assertEqual('description', call_args[3])
        self.assertEqual('2020-10-25', str(call_args[4]))

    @freeze_time('2020-10-25')
    @patch('wdc.runner.start_work_task')
    def test_valid_no_end_time(self, mock_controller):
        self.cli_runner.invoke(cli, ['start', '0800', '--tag', 't1', '--tag', 't2', '--message', 'description'])
        mock_controller.assert_called()

        call_args = mock_controller.call_args.args

        self.assertEqual('0800', str(call_args[0]))
        self.assertEqual(None, call_args[1])
        self.assertEqual('T1,T2', str(call_args[2]))
        self.assertEqual('description', call_args[3])
        self.assertEqual('2020-10-25', str(call_args[4]))
        self.assertIsInstance(call_args[4], WdcFullDate)

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

        self.assertEqual('0800', str(call_args[0]))
        self.assertEqual(None, call_args[1])
        self.assertEqual('', str(call_args[2]))
        self.assertEqual('', call_args[3])
        self.assertEqual('2020-07-25', str(call_args[4]))

    @patch('wdc.runner.start_work_task')
    def test_invalid_start_time(self, mock_controller):
        self.cli_runner.invoke(cli, ['start', '9999'])
        mock_controller.assert_not_called()


class ListWorkTasksFixture(unittest.TestCase):
    def setUp(self):
        self.cli_runner = CliRunner()

    @patch('wdc.runner.list_tasks')
    def test_valid(self, mock_controller):
        mock_controller.return_value = [
            WdcTask(
                id='test_id',
                date=WdcFullDate('2020-10-25'),
                start=WdcTime('0800'),
                end=WdcTime('0900'),
                tags=WdcTags(['t1']),
                description='test_description',
                timestamp='11'
            )
        ]

        result = self.cli_runner.invoke(cli, ['list'])

        self.assertIn('│ test_id │ 2020-10-25 │ 08:00 │ 09:00 │ T1   │ test_descr.. │', result.output)

    @patch('wdc.runner.list_tasks')
    def test_minimal_task_valid(self, mock_controller):
        mock_controller.return_value = [
            WdcTask(
                id='test_id',
                date=WdcFullDate('2020-10-25'),
                start=WdcTime('0800'),
                end=WdcTime('0900'),
                tags=WdcTags([]),
                description='',
                timestamp='11'
            )
        ]

        result = self.cli_runner.invoke(cli, ['list'])

        self.assertIn('│ test_id │ 2020-10-25 │ 08:00 │ 09:00 │      │             │', result.output)

    @patch('wdc.runner.list_tasks')
    def test_no_tasks_found(self, mock_controller):
        mock_controller.return_value = []

        result = self.cli_runner.invoke(cli, ['list'])

        self.assertIn('No tasks found', result.output)


class HelperFunctionsFixture(unittest.TestCase):
    def test_task_to_printout_valid(self):
        test_object = WdcTask(
            id='testId',
            date=WdcFullDate('2020-10-25'),
            start=WdcTime('0800'),
            end=WdcTime('0900'),
            tags=WdcTags(['t1']),
            description='testDescription',
            timestamp='11'
        )

        result = task_to_printout(test_object)

        self.assertSequenceEqual(result, ['testId', '2020-10-25', '08:00', '09:00', 'T1', 'testDescri..'])


class AmendTaskFixture(unittest.TestCase):
    def setUp(self):
        self.cli_runner = CliRunner()

    @patch('wdc.runner.amend_task')
    def test_all_parameters_given(self, mock_controller):
        self.cli_runner.invoke(cli, ['amend', 'id1', '-s', '0800', '-e',
                                     '0900', '-t', 't1', '-m', 'test message', '-d', '2020-10-25'])

        mock_controller.assert_called()

        self.assertEqual('id1', mock_controller.call_args.args[0])
        self.assertEqual('0800', str(mock_controller.call_args.kwargs['start']))
        self.assertEqual('0900', str(mock_controller.call_args.kwargs['end']))
        self.assertEqual('T1', str(mock_controller.call_args.kwargs['tags']))
        self.assertEqual('test message', mock_controller.call_args.kwargs['message'])
        self.assertEqual('2020-10-25', str(mock_controller.call_args.kwargs['date']))

    @patch('wdc.runner.amend_task')
    def test_no_parameters_given(self, mock_controller):
        self.cli_runner.invoke(cli, ['amend', 'id1'])

        mock_controller.assert_called()

        self.assertEqual('id1', mock_controller.call_args.args[0])
        self.assertEqual(None, mock_controller.call_args.kwargs['start'])
        self.assertEqual(None, mock_controller.call_args.kwargs['end'])
        self.assertEqual('', str(mock_controller.call_args.kwargs['tags']))
        self.assertEqual('', mock_controller.call_args.kwargs['message'])
        self.assertEqual(None, mock_controller.call_args.kwargs['date'])

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
        self.assertEqual(None, call_args['date'])
        # Assert that no output for the export is given
        self.assertEqual('', call_args['file_path'])
        # Assert that JSON is selected as the export type
        self.assertEqual(ExportType.JSON, call_args['export_to'])

    @patch('wdc.runner.export_tasks')
    def test_all_options_given(self, mock_controller):
        result = self.cli_runner.invoke(cli,
                                        ['export', '-d', '2020-10-25', '-o', 'export_today.csv', '--csv'])

        self.assertEqual(0, result.exit_code)

        call_args = mock_controller.call_args.kwargs

        # Assert that no date to export is given
        self.assertEqual('2020-10-25', str(call_args['date']))
        # Assert that no output for the export is given
        self.assertEqual('export_today.csv', call_args['file_path'])
        # Assert that JSON is selected as the export type
        self.assertEqual(ExportType.CSV, call_args['export_to'])


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
            WdcTask('0001', WdcFullDate('2020-10-19'), WdcTime('0800'), WdcTime('1015'),
                    WdcTags.from_str('CUST1,task1'), ''),
            WdcTask('0001', WdcFullDate('2020-10-19'), WdcTime('1015'), WdcTime('1030'),
                    WdcTags.from_str('CUST1,BESPR'), ''),
            WdcTask('0001', WdcFullDate('2020-10-19'), WdcTime('1130'), WdcTime('1200'), WdcTags.from_str('LUNCH'),
                    ''),
            WdcTask('0001', WdcFullDate('2020-10-19'), WdcTime('1200'), WdcTime('1600'),
                    WdcTags.from_str('CUST1,task1'), ''),
            WdcTask('0001', WdcFullDate('2020-10-19'), WdcTime('1600'), WdcTime('1700'),
                    WdcTags.from_str('CUST1,tag1,tag2'), ''),
            WdcTask('0001', WdcFullDate('2020-10-20'), WdcTime('0800'), WdcTime('0900'),
                    WdcTags.from_str('CUST1,task3'), ''),
            WdcTask('0001', WdcFullDate('2020-10-20'), WdcTime('0900'), WdcTime('1015'),
                    WdcTags.from_str('CUST1,task1'), ''),
            WdcTask('0001', WdcFullDate('2020-10-20'), WdcTime('1015'), WdcTime('1030'),
                    WdcTags.from_str('CUST1,BESPR'), ''),
            WdcTask('0001', WdcFullDate('2020-10-20'), WdcTime('1130'), WdcTime('1200'), WdcTags.from_str('LUNCH'),
                    ''),
            WdcTask('0001', WdcFullDate('2020-10-20'), WdcTime('1200'), WdcTime('1600'),
                    WdcTags.from_str('CUST1,task1'), ''),
            WdcTask('0001', WdcFullDate('2020-10-20'), WdcTime('1600'), WdcTime('1700'),
                    WdcTags.from_str('CUST1,tag1,tag2'), ''),
            WdcTask('0001', WdcFullDate('2020-10-21'), WdcTime('1000'), WdcTime('1200'), WdcTags.from_str('CUST2'),
                    ''),
            WdcTask('0001', WdcFullDate('2020-10-21'), WdcTime('1200'), WdcTime('1500'),
                    WdcTags.from_str('CUST1,task1'), ''),
        ])

    def test_print(self):
        print_statistics(self.analysis_data)


class MonthStatsFixture(unittest.TestCase):

    def setUp(self):
        self.cli_runner = CliRunner()

    @patch('wdc.runner.stats_for_month')
    def test_no_parameters_given(self, mock_controller):
        mock_controller.return_value = None
        result = self.cli_runner.invoke(cli, ['statm'])

        self.assertEqual(0, result.exit_code)

        self.assertTupleEqual(mock_controller.call_args.args, ())

    @patch('wdc.runner.stats_for_month')
    def test_valid_month_give(self, mock_controller):
        mock_controller.return_value = None
        result = self.cli_runner.invoke(cli, ['statm', '202011'])

        self.assertEqual(0, result.exit_code)

        self.assertTupleEqual(mock_controller.call_args.args, (WdcMonthDate('202011'),))

    @patch('wdc.runner.stats_for_month')
    def test_invalid_month_given(self, mock_controller):
        result = self.cli_runner.invoke(cli, ['statm', 'NotAMoth'])

        self.assertEqual(2, result.exit_code)

        mock_controller.assert_not_called()
