from wdc.helper.io import append_line
from wdc.helper.hash import generate_hash
from wdc.time import WdcTime, today
from datetime import datetime


def start_work_task(start_time: str, end_time: str, tags, description: str, date: str):
    start = WdcTime(start_time)
    end = WdcTime(end_time) if end_time else None
    date = date if date else today()
    row_id = generate_hash(f'{start_time}{end_time}{description}')

    row_data = []
    row_data.append(row_id)
    row_data.append(date)
    row_data.append(str(start))
    if end != None:
        row_data.append(str(end))
    else:
        row_data.append('')
    row_data.append(','.join(map(str, tags)))
    if description != None:
        row_data.append(description)
    else:
        row_data.append('')

    append_line(row_data)
