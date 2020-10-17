import math
from dataclasses import dataclass
from enum import Enum
from typing import List

from wdc.time import timestamp as ts, WdcTime, WdcFullDate


@dataclass
class WdcTask(object):
    id: str
    date: str
    start: str
    end: str
    tags: str
    description: str
    timestamp: str = ts()

    @property
    def start_time(self):
        if self.start == '':
            return WdcTime.zero()
        return WdcTime(self.start)

    @property
    def end_time(self):
        if self.end == '':
            return WdcTime.zero()
        return WdcTime(self.end)

    @property
    def date_obj(self):
        return WdcFullDate(self.date)

    @property
    def slot(self):
        return WdcTimeSlot(self.start_time, self.end_time)

    def __eq__(self, other):
        return self.id == other.id and self.end == other.end and self.start == other.start and self.date == other.date

    def __hash__(self):
        return hash(f'{self.id}-{self.date}-{self.start}-{self.end}')

    def __lt__(self, other):
        return self.start >= other.end


def is_valid(task: WdcTask) -> bool:
    """
    Determines if a WdcTasks is valid as per definition
    :param task: The task instance to be validated
    :return: True if the WdcTask instance is valid, False if not
    """

    if task is None:
        return False

    if not task.id or not task.start or not task.timestamp:
        return False

    return True


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


class WdcDate(object):
    def __init__(self, date):
        self._raw_date = date


class WdcTimeSlotComparison(Enum):
    BEFORE = 1
    AFTER = 2
    OVERLAP = 3
    UNKNOWN = 4


class WdcTimeSlot(object):
    def __init__(self, start: WdcTime, end: WdcTime):
        self.start = start
        self.end = end

    def compare_with(self, other) -> WdcTimeSlotComparison:
        if not isinstance(other, WdcTimeSlot):
            return WdcTimeSlotComparison.UNKNOWN

        # If the two slots have the same start and end time
        if other.end == self.end and other.start == self.start:
            return WdcTimeSlotComparison.OVERLAP

        if self.start < other.start < self.end:
            return WdcTimeSlotComparison.OVERLAP

        if other.end <= self.start:
            return WdcTimeSlotComparison.AFTER

        if other.start >= self.end:
            return WdcTimeSlotComparison.BEFORE

        return WdcTimeSlotComparison.OVERLAP

    def __lt__(self, other):
        return self.compare_with(other) == WdcTimeSlotComparison.BEFORE

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __gt__(self, other):
        return self.compare_with(other) == WdcTimeSlotComparison.AFTER


class WdcTimeSlotDuration(object):
    def __init__(self, time_slot: WdcTimeSlot):
        self._raw_slot = time_slot
        raw_duration = time_slot.end - time_slot.start
        self._duration = int(raw_duration.hours) * 60 + int(raw_duration.minutes)

    @property
    def hours(self):
        return math.floor(self._duration / 60)

    @property
    def minutes(self):
        return self._duration % 60

    def time_str(self):
        return f"{self.hours}:{self.minutes}"

    def time_fraction_str(self):
        return f'{round(self.hours + self.minutes / 60, 2)}'
