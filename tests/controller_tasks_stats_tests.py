import unittest
from unittest.mock import patch

from wdc.controller.tasks import stats_for_week


class GivenAMonthBreakingWeek(unittest.TestCase):
    """Sometimes the beginning and end of a week are in different months"""

    @patch('wdc.controller.tasks.WdcTaskStore')
    def test_foo(self, mock_store):
        """A Week broken into two months is 2020-W35 starting on 2020-08-30 and ending on 2020-09-05"""

        stats_for_week("2021-W35")

        # Assert that two stores are initialized for the two moths
        self.assertEqual(str(mock_store.call_args_list[0][0][0]), "202108")
        self.assertEqual(str(mock_store.call_args_list[1][0][0]), "202109")
