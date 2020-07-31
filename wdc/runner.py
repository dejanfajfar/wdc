import os
from typing import List

import click

import termtables as tt
from colored import fg, bg, attr

from wdc.classes import WdcTask
from wdc.controller.export_import import export_tasks, ExportType
from wdc.time import is_time_valid, is_date_valid, today, WdcTime
from wdc.calculator import calc_workday_end
from wdc.controller.work_day import start_work_task, list_tasks, end_last_task, WdcTaskInfo, get_task_info, amend_task


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


def print_task_info(task_info: WdcTaskInfo):
    def print_section_header(text): return print(
        f'{os.linesep}{fg(0)}{bg(111)}{attr(1)}:: {text} {attr(0)}{os.linesep}')

    def print_task_attribute(attribute, value): return print(f'{attribute} :\t{value}')

    print_section_header('Current')
    current = task_info.current
    print_task_attribute('id         ', current.id)
    print_task_attribute('description', current.description)
    print_task_attribute('timestamp  ', current.timestamp)
    print_task_attribute('start      ', current.start)
    print_task_attribute('end        ', current.end)
    print_task_attribute('tags       ', current.tags)

    print_section_header('History')

    tt.print(
        list(map(lambda i: task_to_history_print(i), task_info.history)),
        header=['Timestamp', 'Date', 'Start', 'End', 'Tags', 'Description'],
        style=tt.styles.rounded_double
    )


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

    wd_end = calc_workday_end(workday_start, break_duration, workday_duration)

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

    start_work_task(task_start, end, list(tag), message, date)


@cli.command('list')
@click.pass_context
@click.option(
    '-d',
    '--date',
    callback=validate_date_callback,
    type=str,
    help='The date for which the tasks should be shown ')
@click.option(
    '-a',
    '--all',
    is_flag=True,
    default=False,
    help='Show duplicates of time entries'
)
def list_all(ctx, date, all):
    tasks = list_tasks(date, all)

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
def info(ctx, task_id):
    task_info = get_task_info(task_id)

    if task_info:
        print_task_info(task_info)
    else:
        print(f'Task with id {task_id} not found.')


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
def export(ctx, date, output, csv):
    selected_export_type = ExportType.JSON
    if csv:
        selected_export_type = ExportType.CSV

    export_tasks(date=date,
                 file_path=output,
                 export_to=selected_export_type)


if __name__ == '__main__':
    cli(obj={})
