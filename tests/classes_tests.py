import unittest

from wdc.classes import WdcTask, to_array, to_task, is_valid


class TaskToArrayFixture(unittest.TestCase):
    def test_valid(self):
        task = WdcTask(
            id='test_id',
            date='2020-10-25',
            start='0800',
            end='0900',
            tags='t1',
            description='description',
            timestamp='1603620000'
        )
        result = to_array(task)

        self.assertSequenceEqual(result, ['test_id', '2020-10-25', '0800', '0900', 't1', 'description', '1603620000'])


class ArrayToTaskFixture(unittest.TestCase):
    def test_valid(self):
        test_array = ['test_id', '2020-10-25', '0800', '0900', 't1', 'description', '11']

        result = to_task(test_array)

        self.assertEqual('test_id', result.id)
        self.assertEqual('2020-10-25', result.date)
        self.assertEqual('0800', result.start)
        self.assertEqual('0900', result.end)
        self.assertEqual('t1', result.tags)
        self.assertEqual('description', result.description),
        self.assertEqual('11', result.timestamp)


class WdcTaskFixture(unittest.TestCase):
    def test_equality_valid(self):
        test_object = WdcTask(
            id='test_id',
            date='2020-10-25',
            start='0800',
            end='0900',
            tags='t1',
            description='description',
            timestamp='11'
        )
        test_object2 = WdcTask(
            id='test_id',
            date='2020-10-25',
            start='0800',
            end='0900',
            tags='t1',
            description='description',
            timestamp='11'
        )

        self.assertTrue(test_object == test_object2)

    def test_equality_different_id_invalid(self):
        test_object = WdcTask(
            id='test_id1',
            date='2020-10-25',
            start='0800',
            end='0900',
            tags='t1',
            description='description',
            timestamp='11'
        )
        test_object2 = WdcTask(
            id='test_id2',
            date='2020-10-25',
            start='0800',
            end='0900',
            tags='t1',
            description='description',
            timestamp='11'
        )

        self.assertFalse(test_object == test_object2)


class IsValidFixture(unittest.TestCase):
    def test_valid_task_ok(self):
        test_object = WdcTask(
            id='test_id1',
            date='2020-10-25',
            start='0800',
            end='0900',
            tags='t1',
            description='description',
            timestamp='11'
        )

        self.assertTrue(is_valid(test_object))

    def test_invalid_start(self):
        test_object = WdcTask(
            id='test_id1',
            date='2020-10-25',
            start='',
            end='0900',
            tags='t1',
            description='description',
            timestamp='11'
        )

        self.assertFalse(is_valid(test_object))

    def test_invalid_id(self):
        test_object = WdcTask(
            id='',
            date='2020-10-25',
            start='0800',
            end='0900',
            tags='t1',
            description='description',
            timestamp='11'
        )

        self.assertFalse(is_valid(test_object))

    def test_invalid_timestamp(self):
        test_object = WdcTask(
            id='test_id1',
            date='2020-10-25',
            start='0800',
            end='0900',
            tags='t1',
            description='description',
            timestamp=''
        )

        self.assertFalse(is_valid(test_object))

    def test_none(self):
        self.assertFalse(is_valid(None))
