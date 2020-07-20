import unittest
from unittest.mock import patch
from click.testing import CliRunner

from wdc.helper.io import WdcTask
from wdc.runner import cli, task_to_printout
from freezegun import freeze_time


class CalcCommandFixture(unittest.TestCase):
    def setUp(self):
        self.cli_runner = CliRunner()

    def test_valid_no_options(self):
        result = self.cli_runner.invoke(cli, ['calc', '0800'])
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
        self.assertIn('Start of the workday time 0860 is an impossible time', result.output)

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
        self.assertEqual(('t1', 't2'), call_args[2])
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
        self.assertEqual(('t1', 't2'), call_args[2])
        self.assertEqual('description', call_args[3])
        self.assertEqual('2020-10-25', call_args[4])

    # def test_go(self):
        # self.cli_runner.invoke(cli, ['start', '0800', '--tag', 't1', '--tag', 't2', '--end',
        #                             '0900', '--message', 'description'])

        result = self.cli_runner.invoke(cli, ['list'])
        print(result.output)

        # result = self.cli_runner.invoke(cli, ['--help'])
        # print(result.output)

    @freeze_time('2020-07-25')
    @patch('wdc.runner.start_work_task')
    def test_valid_only_start(self, mock_controller):
        self.cli_runner.invoke(cli, ['start', '0800'])
        mock_controller.assert_called()

        call_args = mock_controller.call_args.args

        self.assertEqual('0800', call_args[0])
        self.assertEqual('', call_args[1])
        self.assertEqual((), call_args[2])
        self.assertEqual('', call_args[3])
        self.assertEqual('2020-07-25', call_args[4])

    @patch('wdc.runner.start_work_task')
    def test_invalid_start_time(self, mock_controller):
        result = self.cli_runner.invoke(cli, ['start', '9999'])
        self.assertIn('9999', result.output)
        mock_controller.assert_not_called()


class HelperFunctionsFixture(unittest.TestCase):
    def test_ttask_to_printout_valid(self):
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
