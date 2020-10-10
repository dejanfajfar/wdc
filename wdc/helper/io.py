import csv
from os import listdir
from os.path import isfile, join

import wdc.settings as settings
from wdc.classes import WdcTask, to_array, to_task
from wdc.time import is_date_valid, to_date_no_day
from pathlib import Path
from typing import List

HOME_DIR_PATH = Path.joinpath(Path.home(), settings.HOME_DIR)


def task_file_path(date: str):
    if not is_date_valid(date):
        raise ValueError(f'{date} is not a valid date')

    return Path.joinpath(HOME_DIR_PATH, f'{to_date_no_day(date)}.csv')


def write_tasks(tasks: List[WdcTask], date: str = ""):
    HOME_DIR_PATH.mkdir(parents=True, exist_ok=True)

    with open(str(task_file_path(date)), 'w', newline='') as file:
        csv_writer = csv.writer(file, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for task in tasks:
            csv_writer.writerow(to_array(task))


def read_all_tasks(date: str) -> List[WdcTask]:
    if not is_date_valid(date):
        raise ValueError(f'{date} is not a valid date')

    file_path = task_file_path(date)

    if not file_path.exists():
        return []

    with open(str(file_path), 'r') as file:
        return list(map(lambda x: to_task(x), list(csv.reader(file, delimiter=';'))))


def find_tasks(task_id: str) -> List[WdcTask]:

    all_files = [f for f in listdir(HOME_DIR_PATH) if isfile(join(HOME_DIR_PATH, f))]
    work_day_files = list(filter(lambda f: f.endswith('csv'), all_files))

    ret_val = []
    for file in work_day_files:
        with open(Path.joinpath(HOME_DIR_PATH, file), 'r') as openFile:
            tasks = list(map(lambda x: to_task(x), list(csv.reader(openFile, delimiter=';'))))
            for task in tasks:
                if task.id == task_id:
                    ret_val.append(task)

    return sorted(ret_val, key=lambda t: int(t.timestamp))


def write_file(content: str, path: str):
    with open(path, 'w') as openFile:
        openFile.write(content)
