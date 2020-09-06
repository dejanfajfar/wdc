from typing import List

from wdc.classes import WdcTask
from wdc.helper.io import read_all_tasks, write_tasks
from wdc.time import assert_date, today


class WdcTaskStore(object):
    def __init__(self):
        self._tasks: List[WdcTask] = []
        self.is_loaded = False

    def load(self, date: str = today()):
        assert_date(date)
        self._tasks = read_all_tasks(date)
        self.is_loaded = True
        return self

    def save(self):
        self._tasks.sort(key=lambda t: (t.date, t.start))

        write_tasks(self._tasks)

    def add(self, task: WdcTask):
        """
        Adds or updates the given Task
        :param task: The task to add or update
        """
        if not self.is_loaded:
            self.load(task.date)

        if self.contains(task):
            # TODO: Rework to replace the existing task with the new one.
            self._tasks.append(task)
        else:
            self._tasks.append(task)

    def contains(self, task: WdcTask) -> bool:
        for _task in self._tasks:
            if _task.id == task.id:
                return True

        return False
