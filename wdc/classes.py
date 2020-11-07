import math
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from wdc.time import timestamp as ts, WdcTime, WdcFullDate


class WdcTags(object):
    def __init__(self, tags: List[str] = []):
        self._raw_tags = tags

    def __str__(self):
        return ','.join(map(str, self.tags_arr))

    @property
    def tags_arr(self) -> List[str]:
        return sorted(list(map(lambda t: t.upper(), self._raw_tags)))

    @staticmethod
    def from_str(tags_str: str) -> 'WdcTags':
        return WdcTags(tags_str.split(','))

    def is_empty(self) -> bool:
        return self.__str__() == ''


@dataclass
class WdcTask(object):
    id: str
    date: WdcFullDate
    start: WdcTime
    end: Optional[WdcTime]
    tags: WdcTags
    description: str
    timestamp: str = ts()

    @property
    def slot(self) -> 'WdcTimeSlot':
        return WdcTimeSlot(self.start, self.end)

    def __eq__(self, other):
        return self.id == other.id and self.end == other.end and self.start == other.start and self.date == other.date

    def __hash__(self):
        return hash(f'{self.id}-{self.date}-{self.start}-{self.end}')

    def __lt__(self, other):
        return self.start >= other.end

    def is_valid(self) -> bool:
        if not self.id or not self.start or not self.timestamp:
            return False

        return True

    @staticmethod
    def from_str_array(array: List[str]) -> 'WdcTask':
        return WdcTask(
            id=array[0],
            date=WdcFullDate(array[1]),
            start=WdcTime(array[2]),
            end=WdcTime(array[3]) if array[3] != 'None' else None,
            tags=WdcTags.from_str(array[4]),
            description=array[5],
            timestamp=array[6]
        )

    def to_str_array(self) -> List[str]:
        return [
            self.id,
            str(self.date),
            str(self.start),
            str(self.end),
            str(self.tags),
            self.description,
            self.timestamp
        ]


class WdcTimeSlotComparison(Enum):
    BEFORE = 1
    AFTER = 2
    OVERLAP = 3
    UNKNOWN = 4


class WdcTimeSlot(object):
    def __init__(self, start: WdcTime, end: Optional[WdcTime] = None):
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

    def is_ongoing(self) -> bool:
        return self.end is None

    def __lt__(self, other):
        return self.compare_with(other) == WdcTimeSlotComparison.BEFORE

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __gt__(self, other):
        return self.compare_with(other) == WdcTimeSlotComparison.AFTER


class WdcTimeSlotDuration(object):
    def __init__(self, time_slot: WdcTimeSlot = None, duration: int = 0):
        if time_slot:
            raw_duration = time_slot.end - time_slot.start
            self._duration = int(raw_duration.hours) * 60 + int(raw_duration.minutes)
        else:
            self._duration = duration

    @property
    def hours(self) -> int:
        return math.floor(self._duration / 60)

    @property
    def minutes(self) -> int:
        return self._duration % 60

    @property
    def total_minutes(self) -> int:
        return self._duration

    def time_str(self):
        return f"{self.hours:02d}:{self.minutes:02d}"

    def time_fraction_str(self):
        return "{:.2f}".format(self.hours + self.minutes / 60)

    def __str__(self):
        return self.time_str()

    def __add__(self, other):
        if not other or not isinstance(other, WdcTimeSlotDuration):
            return self

        return WdcTimeSlotDuration(duration=self.total_minutes + other.total_minutes)
