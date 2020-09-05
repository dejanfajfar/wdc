from typing import List

from wdc.classes import WdcTask
from wdc.helper.io import read_all_tasks, write_task
from wdc.time import assert_date, today


class WdcTaskStore(object):
    def __init__(self):
        self._date: str = ""
        self._is_loaded = False
        self._tasks: List[WdcTask] = []

    def load(self, date: str = today()):
        assert_date(date)
        self._tasks = read_all_tasks(self._date)
        self._is_loaded = True

        return self

    def save(self):
        self._tasks.sort(key=lambda t: (t.date, t.start))

        for task in self._tasks:
            write_task(task)

    def add(self, task: WdcTask):
        if self.contains(task):
            pass
        return self

    def contains(self, task: WdcTask) -> bool:
        for _task in self._tasks:
            if _task.id == task.id:
                return True

        return False
