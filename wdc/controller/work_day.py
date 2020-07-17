from wdc.helper.io import WdcTask, all_tasks, last_task, write_task
from wdc.helper.hash import generate_hash
from wdc.time import WdcTime, today, is_date_valid, is_time_valid

from typing import List


def start_work_task(start_time: str, end_time: str, tags, description: str, date: str):
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
        tags=','.join(map(str, tags)),
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

    write_task(task)


def list_tasks(date: str) -> List[WdcTask]:
    if not is_date_valid(date):
        raise ValueError(f'{date} is not a valid date format')

    return all_tasks(date)
