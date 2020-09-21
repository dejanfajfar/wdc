from typing import List

from wdc.classes import WdcTask


def would_task_overlap(task: WdcTask, tasks: List[WdcTask]) -> bool:
    if not tasks:
        return False

    return False
