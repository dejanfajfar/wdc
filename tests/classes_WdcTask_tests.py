import unittest

from wdc.classes import WdcTask, WdcTags
from wdc.time import WdcTime, WdcFullDate


class TaskToArrayFixture(unittest.TestCase):
    def test_valid(self):
        task = WdcTask(
            id='test_id',
            date=WdcFullDate('2020-10-25'),
            start=WdcTime('0800'),
            end=WdcTime('0900'),
            tags=WdcTags.from_str('t1'),
            description='description',
            timestamp='1603620000'
        )
        result = task.to_str_array()

        self.assertSequenceEqual(result, ['test_id', '2020-10-25', '0800', '0900', 'T1', 'description', '1603620000'])


class ArrayToTaskFixture(unittest.TestCase):
    def test_valid(self):
        test_array = ['test_id', '2020-10-25', '0800', '0900', 't1', 'description', '11']

        result = WdcTask.from_str_array(test_array)

        self.assertEqual('test_id', result.id)
        self.assertEqual('2020-10-25', str(result.date))
        self.assertEqual('0800', str(result.start))
        self.assertEqual('0900', str(result.end))
        self.assertEqual('T1', str(result.tags))
        self.assertEqual('description', result.description),
        self.assertEqual('11', result.timestamp)


class WdcTaskFixture(unittest.TestCase):
    def test_equality_valid(self):
        test_object = WdcTask(
            id='test_id',
            date=WdcFullDate('2020-10-25'),
            start=WdcTime('0800'),
            end=WdcTime('0900'),
            tags=WdcTags.from_str('t1'),
            description='description',
            timestamp='11'
        )
        test_object2 = WdcTask(
            id='test_id',
            date=WdcFullDate('2020-10-25'),
            start=WdcTime('0800'),
            end=WdcTime('0900'),
            tags=WdcTags.from_str('t1'),
            description='description',
            timestamp='11'
        )

        self.assertTrue(test_object == test_object2)

    def test_equality_different_id_invalid(self):
        test_object = WdcTask(
            id='test_id1',
            date=WdcFullDate('2020-10-25'),
            start=WdcTime('0800'),
            end=WdcTime('0900'),
            tags=WdcTags.from_str('t1'),
            description='description',
            timestamp='11'
        )
        test_object2 = WdcTask(
            id='test_id2',
            date=WdcFullDate('2020-10-25'),
            start=WdcTime('0800'),
            end=WdcTime('0900'),
            tags=WdcTags.from_str('t1'),
            description='description',
            timestamp='11'
        )

        self.assertFalse(test_object == test_object2)


class IsValidFixture(unittest.TestCase):
    def test_valid_task_ok(self):
        test_object = WdcTask(
            id='test_id1',
            date=WdcFullDate('2020-10-25'),
            start=WdcTime('0800'),
            end=WdcTime('0900'),
            tags=WdcTags.from_str('t1'),
            description='description',
            timestamp='11'
        )

        self.assertTrue(test_object.is_valid())

    def test_invalid_id(self):
        test_object = WdcTask(
            id='',
            date=WdcFullDate('2020-10-25'),
            start=WdcTime('0800'),
            end=WdcTime('0900'),
            tags=WdcTags.from_str('t1'),
            description='description',
            timestamp='11'
        )

        self.assertFalse(test_object.is_valid())

    def test_invalid_timestamp(self):
        test_object = WdcTask(
            id='test_id1',
            date=WdcFullDate('2020-10-25'),
            start=WdcTime('0800'),
            end=WdcTime('0900'),
            tags=WdcTags.from_str('t1'),
            description='description',
            timestamp=''
        )

        self.assertFalse(test_object.is_valid())
