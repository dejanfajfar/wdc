from functools import reduce
from typing import List, Dict, Optional

from wdc.classes import WdcTask, WdcTimeSlotDuration
from wdc.time import WdcFullDate, WdcTime


class TaskAnalysisResult(object):
    def __init__(self):
        self._dates = dict()
        self._dates_start = dict()
        self._dates_end = dict()
        self._weeks = dict()
        self._tags_by_tag = dict()
        self._tags_by_date = dict()
        self._total_work_time = None

    @property
    def tags(self) -> Dict[str, Dict[str, WdcTimeSlotDuration]]:
        return self._tags_by_tag

    @property
    def dates(self) -> Dict[WdcFullDate, WdcTimeSlotDuration]:
        return self._dates

    def workday_duration(self, date: WdcFullDate) -> Optional[WdcTimeSlotDuration]:
        return self._dates[date] if date in self._dates else None

    def workday_start(self, date: WdcFullDate) -> Optional[WdcTime]:
        return self._dates_start[date] if date in self._dates_start else None

    def workday_end(self, date: WdcFullDate) -> Optional[WdcTime]:
        return self._dates_end[date] if date in self._dates_end else None

    @property
    def total_work_time(self) -> WdcTimeSlotDuration:
        return self._total_work_time

    def tag_time(self, tag: str) -> Dict[WdcFullDate, WdcTimeSlotDuration]:
        return self._tags_by_tag[tag]

    def tag_total_time(self, tag: str) -> WdcTimeSlotDuration:
        total_time = None
        for date in self._tags_by_tag[tag]:
            if not total_time:
                total_time = self._tags_by_tag[tag][date]
            else:
                total_time += self._tags_by_tag[tag][date]

        return total_time

    def add_work_item_duration(self, date: WdcFullDate, duration: WdcTimeSlotDuration):
        if date not in self._dates:
            self._dates[date] = duration
        else:
            self._dates[date] += duration

        week_number = date.to_week_date()

        if week_number not in self._weeks:
            self._weeks[week_number] = duration
        else:
            self._weeks[week_number] += duration

        if not self._total_work_time:
            self._total_work_time = duration
        else:
            self._total_work_time += duration

    def add_tag_duration(self, tag: str, date: WdcFullDate, duration: WdcTimeSlotDuration):
        if date not in self._tags_by_date:
            self._tags_by_date[date] = dict()

        if tag not in self._tags_by_date[date]:
            self._tags_by_date[date][tag] = duration
        else:
            self._tags_by_date[date][tag] += duration

        if tag not in self._tags_by_tag:
            self._tags_by_tag[tag] = dict()

        if date not in self._tags_by_tag[tag]:
            self._tags_by_tag[tag][date] = duration
        else:
            self._tags_by_tag[tag][date] += duration


def analyse_tasks(tasks: List[WdcTask]) -> 'TaskAnalysisResult':
    task_analysis = TaskAnalysisResult()
    for task in tasks:
        duration = WdcTimeSlotDuration(task.slot)
        task_analysis.add_work_item_duration(task.date_obj, duration)

        for tag in task.tags.split(','):
            task_analysis.add_tag_duration(tag, task.date_obj, duration)

    for date in task_analysis.dates:
        start_wd = reduce(
            lambda t1, t2: t1 if t1.start_time < t2.start_time else t2,
            filter(lambda t: t.date_obj == date, tasks))
        end_wd = reduce(
            lambda t1, t2: t1 if t1.end_time > t2.end_time else t2,
            filter(lambda t: t.date_obj == date, tasks))

        task_analysis._dates_start[date] = start_wd.start_time
        task_analysis._dates_end[date] = end_wd.end_time

    return task_analysis
