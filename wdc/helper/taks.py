from typing import List, Optional

from wdc.classes import WdcTask, WdcTimeSlotComparison
from wdc.time import week_num


def overlaps(task: WdcTask, tasks: List[WdcTask]) -> bool:
    if not tasks:
        return False

    same_day_task_list = list(filter(lambda t: t.date == task.date, tasks))

    if not same_day_task_list:
        return False

    overlapping_tasks = filter(lambda t: t.slot.compare_with(task) == WdcTimeSlotComparison.OVERLAP, tasks)

    return len(list(overlapping_tasks)) != 0


def ongoing(tasks: List[WdcTask]) -> Optional[WdcTask]:
    if not tasks:
        return None

    for internal_task in tasks:
        if internal_task.slot.is_ongoing():
            return internal_task


def task_week_number(task: WdcTask) -> int:
    if not task:
        return 0

    return week_num(str(task.date))
