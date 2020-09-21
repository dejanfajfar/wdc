from typing import List, Callable

from wdc.classes import WdcTask
from wdc.exceptions import TaskOverlapError
from wdc.helper.io import read_all_tasks, write_tasks, find_tasks
from wdc.helper.taks import would_task_overlap
from wdc.time import assert_date


class WdcTaskStore(object):
    def __init__(self, date: str):
        assert_date(date)
        self._tasks = read_all_tasks(date)
        self.is_loaded = True
        self._date = date

    def save(self):
        self._tasks.sort(key=lambda t: (t.date, t.start))

        write_tasks(self._tasks, self._date)

    def add(self, task: WdcTask):
        if not would_task_overlap(task, self._tasks):
            if self.contains(task):
                self._tasks = list(map(lambda t: task if t.id == task.id else t, self._tasks))
            else:
                self._tasks.append(task)
        else:
            raise TaskOverlapError(task.id)

        self.save()

    def get(self, predicate: Callable[[WdcTask], bool] = lambda t: True) -> List[WdcTask]:
        for task in self._tasks:
            if predicate(task):
                yield task

    def last(self):
        return self._tasks[-1]

    def add_and_save(self, task: WdcTask):
        self.add(task)
        self.save()

    def contains(self, task: WdcTask) -> bool:
        for _task in self._tasks:
            if _task.id == task.id:
                return True

        return False


def find_stores(task_id: str) -> List[WdcTaskStore]:
    tasks = find_tasks(task_id)
    task_stores = []
    if tasks:
        for task in tasks:
            task_stores = WdcTaskStore(task.date)

    return task_stores
