from wdc.time import WdcTime


def calculate(start: WdcTime, break_duration: int, duration: WdcTime):

    result = start + duration
    result.add_minutes(break_duration)

    return result
