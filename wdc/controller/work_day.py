from wdc.helper.io import append_line
from wdc.helper.hash import generate_hash
from wdc.time import WdcTime, today, is_date_valid


def start_work_task(start_time: str, end_time: str, tags, description: str, date: str):
    start = WdcTime(start_time)
    end = WdcTime(end_time) if end_time else None

    # If a date is provided then it has to be valid
    if not is_date_valid(date) and date != '':
        raise ValueError('Date in invalid format')
    # When no date is provided then we assume "today"
    date = date if date else today()

    row_id = generate_hash(f'{start_time}{end_time}{description}')

    row_data = []
    row_data.append(row_id)
    row_data.append(date)
    row_data.append(str(start))
    if end is not None:
        row_data.append(str(end))
    else:
        row_data.append('')
    row_data.append(','.join(map(str, tags)))
    if description is not None:
        row_data.append(description)
    else:
        row_data.append('')

    append_line(row_data)
