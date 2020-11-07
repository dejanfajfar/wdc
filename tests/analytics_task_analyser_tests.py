import csv
import os
import unittest

from wdc.analytics.task_analyser import analyse_tasks
from wdc.classes import WdcTask
from wdc.time import WdcFullDate

TEST_DATA_FILENAME = os.path.join(os.path.dirname(__file__), 'data', 'analysis_data.csv')


class AnalyserFixrture_GivenFullTimeSheet(unittest.TestCase):
    def setUp(self) -> None:
        with open(str(TEST_DATA_FILENAME), 'r') as file:
            tasks = list(map(lambda x: WdcTask.from_str_array(x), list(csv.reader(file, delimiter=';'))))
        self._result = analyse_tasks(tasks)

    def test_result_not_none(self):
        self.assertIsNotNone(self._result)

    def test_total_work_time_correct(self):
        self.assertEqual("51:00", self._result.total_work_time.time_str())
        self.assertEqual("51.00", self._result.total_work_time.time_fraction_str())

    def test_totals_per_day_correct(self):
        self.assertEqual("08:30", self._result.dates[WdcFullDate('2020-10-01')].time_str())
        self.assertEqual("08:30", self._result.dates[WdcFullDate('2020-10-02')].time_str())
        self.assertEqual("08:30", self._result.dates[WdcFullDate('2020-10-03')].time_str())
        self.assertEqual("08:30", self._result.dates[WdcFullDate('2020-10-04')].time_str())
        self.assertEqual("08:30", self._result.dates[WdcFullDate('2020-10-05')].time_str())
        self.assertEqual("08:30", self._result.dates[WdcFullDate('2020-10-10')].time_str())

    def test_totals_per_tag(self):
        self.assertEqual("25:30", self._result.tag_total_time('CUS1').time_str())
        self.assertEqual("03:15", self._result.tag_total_time('TASK1').time_str())
