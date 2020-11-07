import json
from enum import Enum

from wdc.classes import WdcTask
from wdc.controller.tasks import list_tasks
from wdc.helper.io import write_file
from wdc.time import today, WdcFullDate


class WdcTaskJsonEncoder(json.JSONEncoder):
    def default(self, o: WdcTask):
        return {
            'id': o.id,
            'timestamp': o.timestamp,
            'date': str(o.date),
            'tags': str(o.tags),
            'start': str(o.start),
            'end': str(o.end),
            'message': o.description
        }


class ExportType(Enum):
    JSON = 1
    CSV = 2


def export_tasks(date: WdcFullDate = None,
                 file_path: str = '',
                 export_to: ExportType = ExportType.JSON) -> str:

    if not date:
        date = WdcFullDate(today())

    if file_path == '':
        file_path = f'./export_{date.to_moth_date()}.{export_to.name}'

    tasks = list_tasks(date)

    task_dump = ''

    if export_to == ExportType.JSON:
        task_dump = json.dumps(tasks, indent=4, cls=WdcTaskJsonEncoder)
    elif export_to == ExportType.CSV:
        for task in tasks:
            task_dump += ';'.join(task.to_str_array()) + '\n'

    write_file(task_dump, file_path)

    return task_dump
