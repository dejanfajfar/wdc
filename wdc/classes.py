from dataclasses import dataclass
from typing import List

from wdc.time import timestamp as ts, is_date_valid, is_time_valid


@dataclass
class WdcTask(object):
    id: str
    date: str
    start: str
    end: str
    tags: str
    description: str
    timestamp: str = ts()

    def is_valid(self) -> bool:
        return is_date_valid(self.date) and is_time_valid(self.start) and is_time_valid(self.end)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


def to_task(array: List[str]) -> WdcTask:
    return WdcTask(
        id=array[0],
        date=array[1],
        start=array[2],
        end=array[3],
        tags=array[4],
        description=array[5],
        timestamp=array[6]
    )


def to_array(task: WdcTask) -> List[str]:
    return [
        task.id,
        task.date,
        task.start,
        task.end,
        task.tags,
        task.description,
        task.timestamp
    ]
