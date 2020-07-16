import csv
import wdc.settings as settings
from wdc.time import today_no_date
from pathlib import Path


def append_line(items: list):

    home_dir_path = Path.joinpath(Path.home(), settings.HOME_DIR)

    home_dir_path.mkdir(parents=True, exist_ok=True)

    with open(Path.joinpath(home_dir_path, f'{today_no_date()}.csv'), 'a', newline='') as file:
        csv_writter = csv.writer(file, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        csv_writter.writerow(items)
