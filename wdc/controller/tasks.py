import secrets
from typing import List, Optional

from wdc.analytics.task_analyser import analyse_tasks
from wdc.classes import WdcTask, WdcTags
from wdc.helper.Ensure import Ensure
from wdc.helper.taks import overlaps, ongoing
from wdc.persistence.task_store import WdcTaskStore, find_stores
from wdc.time import WdcTime, timestamp, current_week_num, week_start, week_end, WdcFullDate, current_month_num, \
    WdcMonthDate


def sort_by_time(tasks: List[WdcTask], descending: bool = False) -> List[WdcTask]:
    # TODO: Implement sorting into the WdcTime and WdcDate objects
    return sorted(tasks, key=lambda t: hash(t.start), reverse=descending)


def start_work_task(start_time: WdcTime, end_time: Optional[WdcTime], tags: WdcTags, description: str,
                    date: WdcFullDate):
    Ensure(start_time).not_none('Start time is not provided')
    Ensure(end_time).is_optional_instance_of(WdcTime, 'end_time is not a Time object')
    Ensure(tags).not_none('Tags container not provided')
    Ensure(date).not_none('Date was not provided').instance_of(
        WdcFullDate).that_is(lambda d: d.is_valid, f'Date {date} is not valid')

    row_id = secrets.token_hex(4)

    new_task = WdcTask(
        id=row_id,
        date=date,
        start=start_time,
        end=end_time,
        tags=tags,
        description=description
    )

    store = WdcTaskStore(date.to_moth_date())
    tasks = list(store.get(lambda t: t.date == new_task.date))

    if overlaps(new_task, tasks):
        # TODO: error handling
        return

    predecessor_task = ongoing(tasks)

    if not predecessor_task:
        store.add_and_save(new_task)
        return

    predecessor_task.end = new_task.start

    store.add(predecessor_task)
    store.add(new_task)
    store.save()


def end_last_task(date: WdcFullDate, time: WdcTime):
    if not time:
        time = WdcTime.now()

    task_store = WdcTaskStore(date.to_moth_date())

    task = task_store.last()

    task.end = time
    task.timestamp = timestamp()

    task_store.add_and_save(task)


def list_tasks(date: WdcFullDate) -> List[WdcTask]:
    Ensure(date).not_none('No date provided').instance_of(WdcFullDate) \
        .that_is(lambda d: d.is_valid, 'Provided date is not valid')

    task_store = WdcTaskStore(date.to_moth_date())

    tasks = task_store.get(lambda t: t.date == date)

    return sorted(tasks, key=lambda t: int(t.timestamp))


def amend_task(task_id: str, tags: WdcTags, start: Optional[WdcTime], end: Optional[WdcTime], message: str = '',
               date: Optional[WdcFullDate] = None):
    Ensure(start).is_optional_instance_of(WdcTime)
    Ensure(end).is_optional_instance_of(WdcTime)
    Ensure(date).is_optional_instance_of(WdcFullDate)

    task_stores = list(find_stores(task_id))

    if not task_stores:
        # If an empty array is returned then we assume that no task with the given Id was found
        raise ValueError(f'The provided task id {task_id} did not resolve to a task')

    task_store = task_stores[0]

    task = list(task_store.get(lambda t: t.id == task_id))[0]

    task.timestamp = timestamp()
    task.tags = str(tags) if not tags.is_empty() else task.tags
    task.start = start if start else task.start
    task.end = end if end else task.end
    task.description = message if message else task.description
    task.date = date if date else task.date

    task_store.add_and_save(task)


def stats_for_week(week_str: str = current_week_num()):
    start_date = week_start(week_str)
    end_date = week_end(week_str)

    if start_date.to_moth_date() != end_date.to_moth_date():
        store1 = WdcTaskStore(start_date.to_moth_date())
        store2 = WdcTaskStore(end_date.to_moth_date())

        tasks = store1.get(lambda t: t.date_obj >= start_date) + store2.get(lambda t: t.date_obj <= end_date)

    else:
        store = WdcTaskStore(start_date.to_moth_date())

        tasks = store.get(lambda t: end_date >= t.date >= start_date)

    return analyse_tasks(list(tasks))


def stats_for_month(month: WdcMonthDate = current_month_num()):
    store = WdcTaskStore(month)

    tasks = store.get()

    return analyse_tasks(list(tasks))
