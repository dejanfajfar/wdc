import os
from typing import List, Optional

import click
import termtables as tt
from colored import fg, bg, attr

from wdc.analytics.task_analyser import TaskAnalysisResult
from wdc.classes import WdcTask, WdcTags
from wdc.controller.calculator import calculate
from wdc.controller.export_import import export_tasks, ExportType
from wdc.controller.tasks import start_work_task, list_tasks, end_last_task, amend_task, stats_for_week
from wdc.exceptions import WdcError, TaskOverlapError
from wdc.time import today, WdcTime, WdcFullDate


def validate_break_duration_callback(ctx, param, value):
    if value < 0:
        raise click.BadParameter(f'Provided break duration of {value} is not a valid break duration')
    else:
        return value


def validate_time_callback(ctx, param, value) -> Optional[WdcTime]:
    if not param.required and value == '':
        return None
    try:
        return WdcTime(value)
    except ValueError as err:
        raise click.BadParameter(err)


def validate_date_callback(ctx, param, value):
    # If the date is not required and not given then leave it as non defined
    if not param.required and value == '':
        return None
    date_obj = WdcFullDate(value)
    return date_obj if date_obj.is_valid() else WdcFullDate(today())


def validate_taskid_callback(ctx, param, value):
    if not param.required and value == '':
        return value
    if value != '':
        return value
    else:
        raise click.BadParameter(f'{value} is not a valid task id')


def task_to_printout(task: WdcTask) -> List[str]:
    return [
        task.id,
        str(task.date),
        f'{task.start.hours}:{task.start.minutes}',
        f'{task.end.hours}:{task.end.minutes}',
        str(task.tags),
        (task.description[:10] + '..') if task.description != '' else task.description
    ]


def task_to_history_print(task: WdcTask) -> List[str]:
    temp_list = task_to_printout(task)
    temp_list.pop(0)
    temp_list[4] = task.description

    temp_list.insert(0, task.timestamp)

    return temp_list


def print_warning(text):
    if not text:
        return

    print(f'{os.linesep}{fg(0)}{bg(214)}\u26a0 {text} {attr(0)}{os.linesep}')


def print_error(text):
    if not text:
        return

    print(f'{os.linesep}{fg(0)}{bg(202)}!! {text} {attr(0)}{os.linesep}')


def print_info(text: str) -> None:
    """
    Prints an information type message to the the stdout
    :param text: The text to be displayed as part of the info message.
                if provided empty string then nothing is displayed
    :return: Nothing
    """
    if not text:
        return

    print(f'{os.linesep}{fg(0)}{bg(164)}info: {text} {attr(0)}{os.linesep}')


def print_week_stats(analysis_results: TaskAnalysisResult) -> None:
    header = ['Date'] + sorted([*analysis_results.tags])
    dates = [*analysis_results.dates]
    data = []

    # TODO: Join the two loops into one
    for date in dates:
        date_tags = [date]
        for tag in sorted([*analysis_results.tags]):
            if tag not in analysis_results.tags.keys() or date not in analysis_results.tags[tag].keys():
                date_tags.append('')
            else:
                date_tags.append(analysis_results.tags[tag][date])

        data.append(date_tags)

    work_day_header = ['Date', 'Start', 'End', 'Duration']
    work_day_data = []

    for date in dates:
        work_day_data.append([
            date,
            analysis_results.workday_start(date),
            analysis_results.workday_end(date),
            analysis_results.workday_duration(date)
        ])

    print(f'{bg(229)}{fg(8)}Statistics for week {attr(0)}')
    print(f'Total work time {bg(12)}{fg(8)}{analysis_results.total_work_time} {attr(0)}')
    tt.print(header=work_day_header, data=work_day_data, style=tt.styles.rounded)
    tt.print(header=header, data=data, style=tt.styles.rounded)


def handle_error(error: WdcError) -> None:
    print_error(error)


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.version_option(version='0.1')
@click.pass_context
def cli(ctx, debug):
    ctx.ensure_object(dict)

    ctx.obj['DEBUG'] = debug


@cli.command()
@click.pass_context
@click.argument(
    'workday_start',
    type=str,
    callback=validate_time_callback)
@click.option(
    '-b',
    '--break_duration',
    default=30,
    show_default=True,
    callback=validate_break_duration_callback,
    type=int,
    help='The optional duration of the lunch break in minutes, must be a positive number')
@click.option(
    '-d',
    '--workday_duration',
    default='0745',
    show_default=True,
    type=str,
    callback=validate_time_callback,
    required=True,
    help='The optional duration of the standard workday given in hhmm format')
def calc(ctx, workday_start: WdcTime, break_duration: int, workday_duration: WdcTime):
    wd_end = calculate(workday_start, break_duration, workday_duration)

    print(wd_end)


@cli.command()
@click.pass_context
@click.argument(
    'task_start',
    type=str,
    callback=validate_time_callback,
    required=True)
@click.option(
    '-t',
    '--tag',
    multiple=True,
    default=[],
    show_default=True,
    help='Optional tags to be applied to the workday task')
@click.option(
    '-m',
    '--message',
    default='',
    show_default=True,
    type=str,
    help='The optional message to be associated with the workday task')
@click.option(
    '-e',
    '--end',
    default='',
    required=False,
    show_default=True,
    type=str,
    callback=validate_time_callback,
    help='The optional time at which the work task was finished')
@click.option(
    '-d',
    '--date',
    default='',
    show_default=True,
    required=True,
    callback=validate_date_callback,
    type=str,
    help='The date at which the task has happened')
def start(ctx, task_start: WdcTime, end: Optional[WdcTime], tag: List[str], message: str, date: WdcFullDate):
    try:
        tags = WdcTags(tag)
        start_work_task(task_start, end, tags, message, date)
    except TaskOverlapError as error:
        print_error(error)


@cli.command('list')
@click.pass_context
@click.option(
    '-d',
    '--date',
    callback=validate_date_callback,
    type=str,
    help='The date for which the tasks should be shown ')
def list_all(ctx, date: WdcFullDate):
    tasks = list_tasks(date)

    tasks_to_print = []
    for task in tasks:
        tasks_to_print.append(task_to_printout(task))

    if not tasks:
        print_warning('No tasks found')
        ctx.exit()

    tt.print(
        tasks_to_print,
        header=['Id', 'Date', 'Start', 'End', 'Tags', 'Description'],
        style=tt.styles.thin_thick
    )


@cli.command()
@click.pass_context
@click.option(
    '-d',
    '--date',
    callback=validate_date_callback,
    type=str,
    help='The date for which the last task should be closed')
@click.option(
    '-e',
    '--end',
    default='',
    show_default=True,
    type=str,
    callback=validate_time_callback,
    help='The time at which the work task was finished')
def end(ctx, date: WdcFullDate, end: WdcTime):
    end_last_task(date, end)


@cli.command()
@click.pass_context
@click.argument(
    'task_id',
    type=str,
    callback=validate_taskid_callback)
@click.option(
    '-s',
    '--start',
    default='',
    show_default=True,
    type=str,
    callback=validate_time_callback,
    help='The optional time at which the work task has started')
@click.option(
    '-t',
    '--tag',
    multiple=True,
    default=[],
    show_default=True,
    help='Optional tags to be applied to the workday task')
@click.option(
    '-m',
    '--message',
    default='',
    show_default=True,
    type=str,
    help='The optional message to be associated with the workday task')
@click.option(
    '-e',
    '--end',
    default='',
    show_default=True,
    type=str,
    callback=validate_time_callback,
    help='The optional time at which the work task was finished')
@click.option(
    '-d',
    '--date',
    default='',
    show_default=True,
    callback=validate_date_callback,
    type=str,
    help='The date at which the task has happened')
def amend(ctx, task_id, start: WdcTime, end: WdcTime, tag: List[str], message: str, date: WdcFullDate):
    try:
        tags = WdcTags(tag)
        amend_task(task_id, tags=tags, start=start, end=end, message=message, date=date)
    except (ValueError, TaskOverlapError) as error:
        print_error(error)


@cli.command()
@click.pass_context
@click.option(
    '-d',
    '--date',
    default='',
    show_default=True,
    callback=validate_date_callback,
    type=str,
    help='The date for which the tasks should be exported')
@click.option(
    '-o',
    '--output',
    default='',
    show_default=True,
    type=str,
    help='The file path to where the export should be written')
@click.option(
    '--csv',
    default=False,
    show_default=True,
    type=bool,
    is_flag=True,
    help='Determines if the export should be formatted as csv')
@click.option(
    '--pipe',
    default=False,
    show_default=True,
    type=bool,
    is_flag=True,
    help='Determines that the content of the exported file should be outputted to stout')
@click.option(
    '-r',
    '--raw',
    default=False,
    type=bool,
    is_flag=True,
    help='Determines of all existing tasks should be returned or only the latest version of each'
)
def export(ctx, date: WdcFullDate, output, csv: bool, pipe: bool, raw: bool):
    selected_export_type = ExportType.JSON
    if csv:
        selected_export_type = ExportType.CSV

    result = ''

    try:
        result = export_tasks(date=date,
                              file_path=output,
                              export_to=selected_export_type)
    except WdcError as error:
        handle_error(error)

    if pipe:
        print(result)


@cli.command('stats-w')
@click.pass_context
@click.argument(
    'week',
    type=str,
    default=''
)
def stats_week(ctx, week):
    if week == '':
        print_week_stats(stats_for_week())
    else:
        print_week_stats(stats_for_week(week))


if __name__ == '__main__':
    cli(obj={})
