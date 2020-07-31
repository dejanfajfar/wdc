from wdc.helper.io import read_all_tasks, last_task, write_task, find_tasks, array_to_tags_string
from wdc.classes import WdcTask
from wdc.helper.hash import generate_hash
from wdc.time import WdcTime, today, is_date_valid, is_time_valid, timestamp

from typing import List


class WdcTaskInfo(object):
    def __init__(self, tasks: List[WdcTask]):
        self._raw_tasks = tasks
        self._raw_tasks.sort(key=lambda t: int(t.timestamp), reverse=True)

    @property
    def current(self) -> WdcTask:
        if len(self._raw_tasks) > 0:
            return self._raw_tasks[0]
        else:
            return None

    @property
    def is_valid(self):
        return True

    @property
    def history(self) -> List[WdcTask]:
        if len(self._raw_tasks) > 1:
            return self._raw_tasks[1:]
        else:
            return []


def sort_by_time(tasks: List[WdcTask], descending: bool = False) -> List[WdcTask]:
    return sorted(tasks, key=lambda t: hash(WdcTime(t.start)), reverse=descending)


def start_work_task(start_time: str, end_time: str, tags: List[str], description: str, date: str):
    start = WdcTime(start_time)
    end = WdcTime(end_time) if end_time else None

    # If a date is provided then it has to be valid
    if not is_date_valid(date) and date != '':
        raise ValueError(f'{date} is not a valid date format')
    # When no date is provided then we assume "today"
    date = date if date else today()

    row_id = generate_hash(f'{start_time}{end_time}{description}')

    task_data = WdcTask(
        id=row_id,
        date=date,
        start=str(start),
        end=str(end) if end is not None else '',
        tags=array_to_tags_string(tags),
        description=description
    )

    write_task(task_data)


def end_last_task(date: str, time: str):
    if not is_date_valid(date):
        raise ValueError(f'{date} is not a valid date format')

    if time == '':
        time = str(WdcTime.now())

    if not is_time_valid(time):
        raise ValueError(f'{date} is not a valid date format')

    task = last_task(date)

    task.end = time
    task.timestamp = timestamp()

    write_task(task)


def list_tasks(date: str, show_all: bool) -> List[WdcTask]:
    if not is_date_valid(date):
        raise ValueError(f'{date} is not a valid date format')

    tasks = read_all_tasks(date)

    tasks = list(filter(lambda t: t.date == date, tasks))

    if show_all:
        return sorted(tasks, key=lambda t: int(t.timestamp))

    else:
        return_tasks = {}
        for task in tasks:
            if task.id not in return_tasks:
                return_tasks[task.id] = task
            else:
                if int(return_tasks[task.id].timestamp) < int(task.timestamp):
                    return_tasks[task.id] = task
                else:
                    continue

        return sort_by_time(return_tasks.values())


def get_task_info(task_id: str) -> WdcTaskInfo:
    if task_id == '':
        return None
    tasks = find_tasks(task_id)

    if not tasks:
        return None

    return WdcTaskInfo(tasks)


def amend_task(task_id: str, tags: List[str] = [], start: str = '', end: str = '', message: str = '', date: str = ''):
    if start != '' and not is_time_valid(start):
        raise ValueError(f'The start time {start} is not a valid time')

    if end != '' and not is_time_valid(end):
        raise ValueError(f'The end time {end} is not a valid time')

    if date != '' and not is_time_valid(date):
        raise ValueError(f'The given date {date} is not valid')

    task_info = get_task_info(task_id)

    if task_info is None:
        raise ValueError(f'The given task id {task_id} did not resolve to a task')

    task = task_info.current

    task.timestamp = timestamp()
    task.tags = array_to_tags_string(tags) if tags else task.tags
    task.start = start if is_time_valid(start) else task.start
    task.end = end if is_time_valid(end) else task.end
    task.description = message if message else task.description
    task.date = date if is_date_valid(date) else task.date

    write_task(task)
