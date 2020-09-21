import unittest
from unittest.mock import patch
from freezegun import freeze_time
from wdc.controller.tasks import start_work_task, list_tasks, amend_task, sort_by_time
from wdc.classes import WdcTask


class StartWorkdayTaskFixture(unittest.TestCase):

    @freeze_time('2019-10-25')
    @patch('wdc.controller.tasks.WdcTaskStore')
    def test_only_start_given(self, mock_storage):
        start_work_task('0800', '', [], '', '')

        mock_storage.return_value.add_and_save.assert_called()

        call_task = mock_storage.return_value.add_and_save.call_args.args[0]

        self.assertEqual('2019-10-25', call_task.date)
        self.assertEqual('0800', call_task.start)
        self.assertEqual('', call_task.end)
        self.assertEqual('', call_task.tags)
        self.assertEqual('', call_task.description)

    @patch('wdc.controller.tasks.WdcTaskStore')
    def test_all_parameters_given(self, mock_storage):
        start_work_task('0800', '0815', ['t1', 't2'], 'description', '2020-10-25')

        mock_storage.return_value.add_and_save.assert_called()
        call_args = mock_storage.return_value.add_and_save.call_args.args[0]

        self.assertEqual('2020-10-25', call_args.date)
        self.assertEqual('0800', call_args.start)
        self.assertEqual('0815', call_args.end)
        self.assertEqual('t1,t2', call_args.tags)
        self.assertEqual('description', call_args.description)

    @patch('wdc.controller.tasks.WdcTaskStore')
    def test_no_end_time_given(self, mock_storage):
        start_work_task('0800', '', ['t1', 't2'], 'description', '2020-10-25')

        mock_storage.return_value.add_and_save.assert_called()
        call_args = mock_storage.return_value.add_and_save.call_args.args[0]

        self.assertEqual('2020-10-25', call_args.date)
        self.assertEqual('0800', call_args.start)
        self.assertEqual('', call_args.end)
        self.assertEqual('t1,t2', call_args.tags)
        self.assertEqual('description', call_args.description)

    @patch('wdc.controller.tasks.WdcTaskStore')
    def test_no_tags_given(self, mock_storage):
        start_work_task('0800', '0815', [], 'description', '2020-10-25')

        mock_storage.return_value.add_and_save.assert_called()
        call_args = mock_storage.return_value.add_and_save.call_args.args[0]

        self.assertEqual('2020-10-25', call_args.date)
        self.assertEqual('0800', call_args.start)
        self.assertEqual('0815', call_args.end)
        self.assertEqual('', call_args.tags)
        self.assertEqual('description', call_args.description)

    @patch('wdc.controller.tasks.WdcTaskStore')
    def test_no_description_given(self, mock_storage):
        start_work_task('0800', '0815', ['t1', 't2'], '', '2020-10-25')

        mock_storage.return_value.add_and_save.assert_called()
        call_args = mock_storage.return_value.add_and_save.call_args.args[0]

        self.assertEqual('2020-10-25', call_args.date)
        self.assertEqual('0800', call_args.start)
        self.assertEqual('0815', call_args.end)
        self.assertEqual('t1,t2', call_args.tags)
        self.assertEqual('', call_args.description)

    @freeze_time('2019-10-25')
    @patch('wdc.controller.tasks.WdcTaskStore')
    def test_no_date_then_today(self, mock_storage):
        start_work_task('0800', '0815', ['t1', 't2'], 'description', '')

        mock_storage.return_value.add_and_save.assert_called()
        call_args = mock_storage.return_value.add_and_save.call_args.args[0]

        self.assertEqual('2019-10-25', call_args.date)
        self.assertEqual('0800', call_args.start)
        self.assertEqual('0815', call_args.end)
        self.assertEqual('t1,t2', call_args.tags)
        self.assertEqual('description', call_args.description)

    def test_invalid_start_time(self):
        self.assertRaises(ValueError, start_work_task, '9999', '', [], '', '')

    def test_invalid_end_time(self):
        self.assertRaises(ValueError, start_work_task, '0800', '9999', [], '', '')

    def test_invalid_date(self):
        self.assertRaises(ValueError, start_work_task, '0800', '', [], '', '9999-99-99')


class ListWorkTasksFixture(unittest.TestCase):
    def test_invalid_date(self):
        self.assertRaises(ValueError, list_tasks, '9999-99-99')
        self.assertRaises(ValueError, list_tasks, '')

    @patch('wdc.controller.tasks.WdcTaskStore')
    def test_task_are_sorted(self, mock_store):
        mock_store.return_value.get.return_value = [
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

        results = list_tasks('2020-10-25')

        self.assertEqual(2, len(results))
        self.assertEqual('task2', results[0].id)
        self.assertEqual('task1', results[1].id)


class AmendTaskFixture(unittest.TestCase):

    @patch('wdc.controller.tasks.WdcTaskStore')
    @patch('wdc.controller.tasks.find_stores')
    def test_replace_all(self, mock_finder, mock_store):
        mock_store.return_value.get.return_value = [
            WdcTask(
                id='c411c941',
                date='2020-10-25',
                start='0930',
                end='1000',
                tags='home',
                description='test description',
                timestamp='1595423306302'
            )
        ]
        mock_finder.return_value = [mock_store.return_value]

        amend_task('c411c941', tags=['t1', 't2'], start='1000', end='1130', message='test message', date='2020-08-18')

        call_args = mock_store.return_value.add_and_save.call_args.args[0]

        self.assertEqual('c411c941', call_args.id)
        self.assertEqual('t1,t2', call_args.tags)
        self.assertEqual('1000', call_args.start)
        self.assertEqual('1130', call_args.end)
        self.assertEqual('test message', call_args.description)
        self.assertEqual('2020-08-18', call_args.date)

    @patch('wdc.controller.tasks.WdcTaskStore')
    @patch('wdc.controller.tasks.find_stores')
    def test_none_replaced(self, mock_finder, mock_store):
        mock_store.return_value.get.return_value = [
            WdcTask(
                id='c411c941',
                date='2020-10-25',
                start='0930',
                end='1000',
                tags='home',
                description='test description',
                timestamp='1595423306302'
            )
        ]
        mock_finder.return_value = [mock_store.return_value]

        amend_task('c411c941', tags=[], start='', end='', message='', date='')

        call_args = mock_store.return_value.add_and_save.call_args.args[0]

        self.assertEqual('c411c941', call_args.id)
        self.assertEqual('home', call_args.tags)
        self.assertEqual('0930', call_args.start)
        self.assertEqual('1000', call_args.end)
        self.assertEqual('2020-10-25', call_args.date)
        self.assertEqual('test description', call_args.description)

    def test_invalid_start_time(self):
        self.assertRaises(ValueError, amend_task, 'c411c941', [], '9999', '', '', '')

    def test_invalid_end_time(self):
        self.assertRaises(ValueError, amend_task, 'c411c941', [], '', '9999', '', '')

    def test_invalid_date(self):
        self.assertRaises(ValueError, amend_task, 'c411c941', [], '', '', '', '9999-99-99')


class SortTasksByTimeFixture(unittest.TestCase):
    def test_valid_ascending(self):
        test_object = [WdcTask(
            id='1',
            date='2020-10-25',
            start='0800',
            end='0900',
            tags='t1',
            description='description',
            timestamp='11'
        ),
            WdcTask(
            id='2',
            date='2020-10-25',
            start='1000',
            end='1100',
            tags='t1',
            description='description',
            timestamp='2'
        ),
            WdcTask(
            id='3',
            date='2020-10-25',
            start='0900',
            end='1000',
            tags='t1',
            description='description',
            timestamp='33'
        )]

        result = sort_by_time(test_object)

        self.assertEqual('1', result[0].id)
        self.assertEqual('3', result[1].id)
        self.assertEqual('2', result[2].id)

    def test_valid_descending(self):
        test_object = [WdcTask(
            id='1',
            date='2020-10-25',
            start='0800',
            end='0900',
            tags='t1',
            description='description',
            timestamp='11'
        ),
            WdcTask(
            id='2',
            date='2020-10-25',
            start='1000',
            end='1100',
            tags='t1',
            description='description',
            timestamp='2'
        ),
            WdcTask(
            id='3',
            date='2020-10-25',
            start='0900',
            end='1000',
            tags='t1',
            description='description',
            timestamp='33'
        )]

        result = sort_by_time(test_object, descending=True)

        self.assertEqual('2', result[0].id)
        self.assertEqual('3', result[1].id)
        self.assertEqual('1', result[2].id)
