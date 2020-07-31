import json
from enum import Enum

from wdc.classes import WdcTask, to_array
from wdc.helper.io import read_all_tasks, write_file
from wdc.time import today, to_date_no_day


class WdcTaskJsonEncoder(json.JSONEncoder):
    def default(self, o: WdcTask):
        return {
            'id': o.id,
            'timestamp': o.timestamp,
            'tags': o.tags,
            'start': o.start,
            'end': o.end,
            'message': o.description
        }


class ExportType(Enum):
    JSON = 1
    CSV = 2


def export_tasks(date: str = '', file_path: str = '', export_to: ExportType = ExportType.JSON) -> str:
    if date == '':
        date = today()

    if file_path == '':
        file_path = f'./export_{to_date_no_day(date)}.{export_to.name}'

    tasks = read_all_tasks(date)

    task_dump = ''

    if export_to == ExportType.JSON:
        task_dump = json.dumps(tasks, indent=4, cls=WdcTaskJsonEncoder)
    elif export_to == ExportType.CSV:
        for task in tasks:
            task_dump += ';'.join(to_array(task)) + '\n'

    write_file(task_dump, file_path)

    return task_dump
