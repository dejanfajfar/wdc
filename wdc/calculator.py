from wdc.time import WdcTime


def calc_workday_end(start_time: str, break_duration: int, workday_duration: str):
    start = WdcTime(start_time)
    duration = WdcTime(workday_duration)

    result = start + duration
    result.add_minutes(break_duration)

    return result
