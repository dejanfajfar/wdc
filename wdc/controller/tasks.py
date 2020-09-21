import secrets

from wdc.helper.io import array_to_tags_string
from wdc.classes import WdcTask
from wdc.persistence.task_store import WdcTaskStore, find_stores
from wdc.time import WdcTime, today, is_date_valid, is_time_valid, timestamp

from typing import List


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

    row_id = secrets.token_hex(4)

    new_task = WdcTask(
        id=row_id,
        date=date,
        start=str(start),
        end=str(end) if end is not None else '',
        tags=array_to_tags_string(tags),
        description=description
    )

    WdcTaskStore(new_task.date).add_and_save(new_task)


def end_last_task(date: str, time: str = WdcTime.now()):
    if not is_date_valid(date):
        raise ValueError(f'{date} is not a valid date format')

    if not is_time_valid(time):
        raise ValueError(f'{date} is not a valid date format')

    task_store = WdcTaskStore(date)

    task = task_store.last()

    task.end = time
    task.timestamp = timestamp()

    task_store.add_and_save(task)


def list_tasks(date: str) -> List[WdcTask]:
    if not is_date_valid(date):
        raise ValueError(f'{date} is not a valid date format')

    task_store = WdcTaskStore(date)

    tasks = task_store.get(lambda t: t.date == date)

    return sorted(tasks, key=lambda t: int(t.timestamp))


def amend_task(task_id: str, tags: List[str] = [], start: str = '', end: str = '', message: str = '', date: str = ''):
    if start != '' and not is_time_valid(start):
        raise ValueError(f'The start time {start} is not a valid time')

    if end != '' and not is_time_valid(end):
        raise ValueError(f'The end time {end} is not a valid time')

    if date != '' and not is_time_valid(date):
        raise ValueError(f'The given date {date} is not valid')

    task_stores = find_stores(task_id)

    if not task_stores:
        # If an empty array is returned then we assume that no task with the given Id was found
        raise ValueError(f'The provided task id {task_id} did not resolve to a task')

    task_store = task_stores[0]

    task = task_store.get(lambda t: t.id == task_id)[0]

    task.timestamp = timestamp()
    task.tags = array_to_tags_string(tags) if tags else task.tags
    task.start = start if is_time_valid(start) else task.start
    task.end = end if is_time_valid(end) else task.end
    task.description = message if message else task.description
    task.date = date if is_date_valid(date) else task.date

    task_store.add_and_save(task)