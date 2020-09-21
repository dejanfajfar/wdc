class WdcError(Exception):
    pass


class TimeFormatError(WdcError):
    """
    Represents a error with the time format

    Attributes:
        time -- The time that caused the exception
    """

    def __init__(self, time: str):
        self.time = time
        self.message = f'The string {self.time} does not represent a valid time'
        super().__init__(self.message)


class DateFormatError(WdcError):
    """
    Represents a error with the date format

    Attributes:
        date -- The date string that caused the exception
    """

    def __init__(self, date: str):
        self.date = date
        self.message = f'The string {date} does not represent a valid date'
        super().__init__(self.message)


class TaskOverlapError(WdcError):
    def __init__(self, task_id: str):
        self.task_id = task_id
        self.message = f'The task {task_id} overlaps with existing tasks'
        super().__init__(self.message)
