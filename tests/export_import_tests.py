import json
import unittest
from unittest.mock import patch

from wdc.classes import WdcTask, WdcTags
from wdc.controller.export_import import WdcTaskJsonEncoder, export_tasks, ExportType
from wdc.time import WdcFullDate, WdcTime


class WdcTaskJsonEncoderFixture(unittest.TestCase):
    def test_encode_single_instance(self):
        test_object = WdcTask(
            id='c411c941',
            date=WdcFullDate('2020-10-25'),
            start=WdcTime('0930'),
            end=WdcTime('1000'),
            tags=WdcTags(['home']),
            description='test description',
            timestamp='1595423306302'
        )
        result = json.dumps(test_object, indent=4, cls=WdcTaskJsonEncoder)

        self.assertEqual("""{
    "id": "c411c941",
    "timestamp": "1595423306302",
    "date": "2020-10-25",
    "tags": "HOME",
    "start": "0930",
    "end": "1000",
    "message": "test description"
}""", result)

    def test_encode_list(self):
        test_object = [WdcTask(
            id='c411c941',
            date=WdcFullDate('2020-10-25'),
            start=WdcTime('0930'),
            end=WdcTime('1000'),
            tags=WdcTags(['home']),
            description='test description',
            timestamp='1595423306302'
        ),
            WdcTask(
            id='c411c941',
            date=WdcFullDate('2020-10-25'),
            start=WdcTime('0930'),
            end=WdcTime('1000'),
            tags=WdcTags(['home']),
            description='test description',
            timestamp='1595423306302'
        )]

        result = json.dumps(test_object, indent=4, cls=WdcTaskJsonEncoder)

        self.assertEqual("""[
    {
        "id": "c411c941",
        "timestamp": "1595423306302",
        "date": "2020-10-25",
        "tags": "HOME",
        "start": "0930",
        "end": "1000",
        "message": "test description"
    },
    {
        "id": "c411c941",
        "timestamp": "1595423306302",
        "date": "2020-10-25",
        "tags": "HOME",
        "start": "0930",
        "end": "1000",
        "message": "test description"
    }
]""", result)


class ExportTasksFixture(unittest.TestCase):

    @patch('wdc.controller.export_import.today')
    @patch('wdc.controller.export_import.list_tasks')
    @patch('wdc.controller.export_import.write_file')
    def test_default_parameters(self, mock_writer, mock_reader, mock_today):
        mock_today.return_value = '2020-10-25'
        mock_reader.return_value = [WdcTask(
            id='c411c941',
            date=WdcFullDate('2020-10-25'),
            start=WdcTime('0930'),
            end=WdcTime('1000'),
            tags=WdcTags(['home']),
            description='test description',
            timestamp='1595423306302'
        )]

        expected_dump = """[
    {
        "id": "c411c941",
        "timestamp": "1595423306302",
        "date": "2020-10-25",
        "tags": "HOME",
        "start": "0930",
        "end": "1000",
        "message": "test description"
    }
]"""
        result = export_tasks()

        self.assertIn(expected_dump, mock_writer.call_args.args[0])
        self.assertIn('export_202010.JSON', mock_writer.call_args.args[1])
        self.assertIn(expected_dump, result)

    @patch('wdc.controller.export_import.today')
    @patch('wdc.controller.export_import.list_tasks')
    @patch('wdc.controller.export_import.write_file')
    def test_fully_qualified_parameters(self, mock_writer, mock_reader, mock_today):
        mock_today.return_value = '2020-10-25'
        mock_reader.return_value = [WdcTask(
            id='c411c941',
            date=WdcFullDate('2020-10-25'),
            start=WdcTime('0930'),
            end=WdcTime('1000'),
            tags=WdcTags(['home']),
            description='test description',
            timestamp='1595423306302'
        )]

        expected_dump = """[
    {
        "id": "c411c941",
        "timestamp": "1595423306302",
        "date": "2020-10-25",
        "tags": "HOME",
        "start": "0930",
        "end": "1000",
        "message": "test description"
    }
]"""
        result = export_tasks('2020-08-18', 'myexport.json', ExportType.JSON)

        self.assertEqual('2020-08-18', mock_reader.call_args.args[0])
        mock_today.assert_not_called()
        self.assertIn(expected_dump, mock_writer.call_args.args[0])
        self.assertIn('myexport.json', mock_writer.call_args.args[1])
        self.assertIn(expected_dump, result)

    @patch('wdc.controller.export_import.today')
    @patch('wdc.controller.export_import.list_tasks')
    @patch('wdc.controller.export_import.write_file')
    def test_csv_default_parameters(self, mock_writer, mock_reader, mock_today):
        mock_today.return_value = '2020-10-25'
        mock_reader.return_value = [WdcTask(
            id='c411c941',
            date=WdcFullDate('2020-10-25'),
            start=WdcTime('0930'),
            end=WdcTime('1000'),
            tags=WdcTags(['home']),
            description='test description',
            timestamp='1595423306302'
        )]

        expected_dump = """c411c941;2020-10-25;0930;1000;HOME;test description;1595423306302"""
        result = export_tasks(export_to=ExportType.CSV)

        self.assertIn(expected_dump, mock_writer.call_args.args[0])
        self.assertIn('export_202010.CSV', mock_writer.call_args.args[1])
        self.assertIn(expected_dump, result)

    @patch('wdc.controller.export_import.today')
    @patch('wdc.controller.export_import.list_tasks')
    @patch('wdc.controller.export_import.write_file')
    def test_csv_default_parameters_multiple_tasks(self, mock_writer, mock_reader, mock_today):
        mock_today.return_value = '2020-10-25'
        mock_reader.return_value = [WdcTask(
            id='c411c941',
            date=WdcFullDate('2020-10-25'),
            start=WdcTime('0930'),
            end=WdcTime('1000'),
            tags=WdcTags(['home']),
            description='test description',
            timestamp='1595423306302'
        ),
            WdcTask(
                id='c411c942',
                date=WdcFullDate('2020-10-25'),
                start=WdcTime('0930'),
                end=WdcTime('1000'),
                tags=WdcTags(['home']),
                description='test description1',
                timestamp='1595423306303'
        )
        ]

        expected_dump = """c411c941;2020-10-25;0930;1000;HOME;test description;1595423306302
c411c942;2020-10-25;0930;1000;HOME;test description1;1595423306303"""
        result = export_tasks(export_to=ExportType.CSV)

        self.assertIn(expected_dump, mock_writer.call_args.args[0])
        self.assertIn('export_202010.CSV', mock_writer.call_args.args[1])
        self.assertIn(expected_dump, result)
