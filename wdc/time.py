import re
from datetime import datetime


def is_time_valid(time: str) -> bool:
    return re.match(r"(([01][0-9])|(2[0-3]))[0-5][0-9]", time)


def is_date_valid(date: str) -> bool:
    return re.match(r"(19|20)\d\d-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])", date)


def today() -> str:
    now = datetime.now()
    return now.strftime('%Y-%m-%d')


def today_no_date() -> str:
    now = datetime.now()
    return now.strftime('%Y%m')


class WdcTime(object):

    def __init__(self, time):
        if is_time_valid(time):
            self.__rawTime = time
        else:
            raise ValueError("{0} must be between 0 and 2359".format(time))

    @property
    def minutes(self):
        return self.__rawTime[2:4]

    @property
    def hours(self):
        return self.__rawTime[0:2]

    def __add__(self, addend):
        addend_minutes = int(addend.minutes)
        addend_hours = int(addend.hours)

        sum = WdcTime(self.__rawTime)
        sum.add_minutes(addend_minutes)
        sum.add_hours(addend_hours)

        return sum

    def add_hours(self, hours: int):
        time_hours = int(self.hours)
        new_hours = (time_hours + hours) % 24

        # There is no hour 24 this is automaticall converted to 00
        if new_hours == "24":
            new_hours = "00"
        self.__rawTime = f"{new_hours:02d}{self.minutes}"
        return self

    def add_minutes(self, minutes: int):
        self_minutes = int(self.minutes)

        new_minutes = (self_minutes + minutes) % 60
        if new_minutes == "60":
            new_minutes = "00"

        self.__rawTime = f"{self.hours}{new_minutes:02d}"

        # Carry the hour if the sum of minutes is more than 60
        if (self_minutes + minutes) // 60 != 0:
            self.add_hours((self_minutes + minutes) // 60)
        return self

    def __str__(self):
        return self.__rawTime
