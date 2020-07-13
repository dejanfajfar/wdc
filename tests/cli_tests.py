import unittest

from click.testing import CliRunner
from wdc.runner import cli


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
