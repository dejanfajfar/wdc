import os
from typing import List

import click

import termtables as tt
from colored import fg, bg, attr

from wdc.classes import WdcTask
from wdc.controller.export_import import export_tasks, ExportType
from wdc.exceptions import WdcError, TaskOverlapError
from wdc.time import is_time_valid, is_date_valid, today, WdcTime
from wdc.controller.calculator import calculate
from wdc.controller.tasks import start_work_task, list_tasks, end_last_task, amend_task


def validate_break_duration_callback(ctx, param, value):
    if value < 0:
        raise click.BadParameter(f'Provided break duration of {value} is not a valid break duration')
    else:
        return value


def validate_time_callback(ctx, param, value):
    if not param.required and value == '':
        return value
    if is_time_valid(value):
        return value
    else:
        raise click.BadParameter(f'{value} is not a valid time')


def validate_date_callback(ctx, param, value):
    if not param.required and value == '':
        return value
    if is_date_valid(value):
        return value
    else:
        return today()


def validate_taskid_callback(ctx, param, value):
    if not param.required and value == '':
        return value
    if value != '':
        return value
    else:
        raise click.BadParameter(f'{value} is not a valid task id')


def task_to_printout(task: WdcTask) -> List[str]:
    start = WdcTime(task.start)
    if task.end != '':
        end = WdcTime(task.end)

    return [
        task.id,
        task.date,
        f'{start.hours}:{start.minutes}',
        f'{end.hours}:{end.minutes}' if task.end != '' else task.end,
        task.tags,
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
def calc(ctx, workday_start, break_duration, workday_duration):
    wd_end = calculate(workday_start, break_duration, workday_duration)

    print(wd_end)


@cli.command()
@click.pass_context
@click.argument(
    'task_start',
    type=str,
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
def start(ctx, task_start, end, tag, message, date):
    if not is_time_valid(task_start):
        print_error(f'Start time {task_start} of the task is an impossible time')
        ctx.exit()

    try:
        start_work_task(task_start, end, list(tag), message, date)
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
def list_all(ctx, date):
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
def end(ctx, date, end):
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
def amend(ctx, task_id, start, end, tag, message, date):
    try:
        amend_task(task_id, tags=list(tag), start=start, end=end, message=message, date=date)
    except ValueError as error:
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
def export(ctx, date, output, csv, pipe, raw):
    """
    The Export command implementation

    :param ctx: The cli app context
    :param date: The optional date to be exported (default is today)
    :param output: The optional output file to which the tasks are to be exported
    :param csv: Flag to denote that the export format should be CSV
    :param pipe: A flag denoting that the export file content should be printed onto the stout stream
    :param raw: If False then export only the latest version of each task. All if True
    :return: Nothing
    """
    selected_export_type = ExportType.JSON
    if csv:
        selected_export_type = ExportType.CSV

    result = ''

    try:
        result = export_tasks(date=date,
                              file_path=output,
                              export_to=selected_export_type,
                              export_all=raw)
    except WdcError as error:
        handle_error(error)

    if pipe:
        print(result)


@cli.command()
@click.pass_context
def stats(ctx):
    pass


if __name__ == '__main__':
    cli(obj={})
