import re
from datetime import datetime
from time import time
from typing import Optional

from wdc.exceptions import TimeFormatError, DateFormatError

DATE_FORMAT = '%Y-%m-%d'
DATE_REGEX = r"(19|20)\d\d-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])"
MONTH_FORMAT = '%Y%m'
MONTH_REGEX = r"^\d{4}0?(0[1-9]|1[012])$"
WEEK_FORMAT = '%G-W%V'


def assert_time(time_str: str) -> None:
    if not is_time_valid(time_str):
        raise TimeFormatError(time_str)


def assert_date(date_str: str) -> None:
    if not re.match(DATE_REGEX, date_str) and not re.match(MONTH_REGEX, date_str):
        raise DateFormatError(date_str)


def is_time_valid(time_str: str) -> bool:
    if time_str is None:
        return False
    return re.match(r"(([01][0-9])|(2[0-3]))[0-5][0-9]", time_str) is not None


def is_date_valid(date_str: str) -> bool:
    if date_str is None:
        return False
    return re.match(r"(19|20)\d\d-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])", date_str) is not None


def today() -> str:
    now = datetime.now()
    return now.strftime(DATE_FORMAT)


def to_date_no_day(date_str: str) -> str:
    assert_date(date_str)

    date = datetime.strptime(date_str, DATE_FORMAT)

    return date.strftime(MONTH_FORMAT)


def timestamp() -> str:
    return str(int(time() * 1000))


def current_week_num() -> str:
    return datetime.now().strftime(WEEK_FORMAT)


def is_week_num_valid(week_num_str: str) -> bool:
    if week_num_str is None:
        return False
    return re.match(r"\d{4}-W\d{2}", week_num_str) is not None


def parse_date_str(date_str: str) -> Optional[datetime]:
    if not is_date_valid(date_str):
        return None
    return datetime.strptime(date_str, DATE_FORMAT)


def week_num(date_str: str) -> int:
    date_time = parse_date_str(date_str)
    if not date_time:
        return 0
    return date_time.isocalendar()[1]


def week_start(week_number: str) -> Optional['WdcFullDate']:
    if not is_week_num_valid(week_number):
        return None
    return WdcFullDate(date_time=datetime.strptime(week_number + '-1', '%G-W%V-%w'))


def week_end(week_number: str) -> Optional['WdcFullDate']:
    if not is_week_num_valid(week_number):
        return None
    return WdcFullDate(date_time=datetime.strptime(week_number + '-0', '%G-W%V-%w'))


class WdcDate(object):
    def __init__(self, format_string: str, regex: str, date_str: str = None):
        self.__date_format_string = format_string
        self.__date_regex = regex
        self.__raw_date_str = date_str

    def is_valid(self) -> bool:
        if self.__raw_date_str is None:
            return False
        return re.match(self.__date_regex, self.__raw_date_str) is not None

    def ensure_valid(self) -> None:
        if not self.is_valid():
            raise DateFormatError(self.__raw_date_str)

    def __str__(self):
        return self.__raw_date_str

    def __eq__(self, other):
        if not isinstance(other, WdcDate):
            return False
        return self.__raw_date_str == other.__raw_date_str


class WdcFullDate(WdcDate):
    def __init__(self, date_str: str = None, date_time: datetime = None):
        if not date_str and date_str != '':
            super().__init__(DATE_FORMAT, DATE_REGEX,
                             (date_time if date_time else datetime.now()).strftime(DATE_FORMAT))
        else:
            super().__init__(DATE_FORMAT, DATE_REGEX, date_str)

    def to_moth_date(self) -> 'WdcMonthDate':
        date_time = datetime.strptime(str(self), DATE_FORMAT)

        return WdcMonthDate(date_time.strftime(MONTH_FORMAT))


class WdcMonthDate(WdcDate):
    def __init__(self, date_str: str = None, date_time: datetime = None):
        if not date_str and date_str != '':
            super().__init__(MONTH_FORMAT, MONTH_REGEX,
                             (date_time if date_time else datetime.now()).strftime(MONTH_FORMAT))
        else:
            super().__init__(MONTH_FORMAT, MONTH_REGEX, date_str)


class WdcTime(object):

    def __init__(self, time):
        if is_time_valid(time):
            self.__rawTime = time
        else:
            raise ValueError("{0} must be between 0 and 2359".format(time))

    @staticmethod
    def now():
        now = datetime.now()
        return WdcTime(f'{now.hour:02d}{now.minute:02d}')

    @staticmethod
    def zero():
        return WdcTime('0000')

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

        # There is no hour 24 this is automatically converted to 00
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

    def __hash__(self):
        return (int(self.hours) * 100) + int(self.minutes)

    def __str__(self):
        return self.__rawTime

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __lt__(self, other):
        return hash(self) < hash(other)

    def __gt__(self, other):
        return hash(self) > hash(other)

    def __le__(self, other):
        return hash(self) <= hash(other)

    def __ge__(self, other):
        return hash(self) >= hash(other)

    def __sub__(self, other):
        newTime = WdcTime(self.__rawTime)

        newTime.add_hours(-1 * int(other.hours))
        newTime.add_minutes(-1 * int(other.minutes))

        return newTime
