import csv
import wdc.settings as settings
from wdc.time import is_date_valid, is_time_valid, to_date_no_day, timestamp as ts
from pathlib import Path
from dataclasses import dataclass
from typing import List

HOME_DIR_PATH = Path.joinpath(Path.home(), settings.HOME_DIR)


@dataclass
class WdcTask(object):
    id: str
    date: str
    start: str
    end: str
    tags: str
    description: str
    timestamp: str = ts()

    def is_valid(self) -> bool:
        return is_date_valid(self.date) and is_time_valid(self.start) and is_time_valid(self.end)


def array_to_task(array: List[str]) -> WdcTask:
    return WdcTask(
        id=array[0],
        date=array[1],
        start=array[2],
        end=array[3],
        tags=array[4],
        description=array[5]
    )


def task_to_array(task: WdcTask) -> List[str]:
    return [
        task.id,
        task.date,
        task.start,
        task.end,
        task.tags,
        task.description,
        task.timestamp
    ]


def task_file_path(date: str):
    if not is_date_valid(date):
        raise ValueError(f'{date} is not a valid date')

    return Path.joinpath(HOME_DIR_PATH, f'{to_date_no_day(date)}.csv')


def write_task(task: WdcTask):
    # TODO: add capability to amend existing task
    HOME_DIR_PATH.mkdir(parents=True, exist_ok=True)

    with open(task_file_path(task.date), 'a', newline='') as file:
        csv_writter = csv.writer(file, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        csv_writter.writerow(task_to_array(task))


def last_task(date: str) -> WdcTask:
    if not is_date_valid(date):
        raise ValueError(f'{date} is not a valid date')

    file_path = task_file_path(date)

    if not file_path.exists():
        raise FileNotFoundError(str(file_path))

    with open(file_path, 'r') as file:
        row = list(csv.reader(file, delimiter=';'))[-1]
        return array_to_task(row)


def all_tasks(date: str) -> List[WdcTask]:
    if not is_date_valid(date):
        raise ValueError(f'{date} is not a valid date')

    file_path = task_file_path(date)

    if not file_path.exists():
        raise FileNotFoundError(str(file_path))

    with open(file_path, 'r') as file:
        return list(map(lambda x: array_to_task(x), list(csv.reader(file, delimiter=';'))))
