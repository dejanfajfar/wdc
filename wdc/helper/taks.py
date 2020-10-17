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


def predecessors(task: WdcTask, tasks: List[WdcTask]) -> List[WdcTask]:
    for inline_task in tasks:
        slot_comparison = inline_task.slot.compare_with(task.slot)
        if slot_comparison == WdcTimeSlotComparison.BEFORE:
            yield inline_task


def predecessor(task: WdcTask, tasks: List[WdcTask]) -> Optional[WdcTask]:
    if not tasks:
        return None

    predecessors_list = sorted(predecessors(task, tasks), key=lambda t: t.slot)
    if predecessors_list:
        return predecessors_list[-1]
    return None


def task_week_number(task: WdcTask) -> int:
    if not task:
        return 0

    return week_num(task.date)
