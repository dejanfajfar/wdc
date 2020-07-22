import click

import termtables as tt

from wdc.helper.io import WdcTask
from wdc.time import is_time_valid, is_date_valid, today, WdcTime
from wdc.calculator import calc_workday_end
from wdc.controller.work_day import start_work_task, list_tasks, end_last_task


def validate_time_callback(ctx, param, value):
    if not param.required and value == '':
        return value
    if is_time_valid(value):
        return value
    else:
        raise click.BadParameter(f'{value} is not a valid time')


def validate_date_callback(ctx, param, value):
    if is_date_valid(value):
        return value
    else:
        return today()


def task_to_printout(task: WdcTask):
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
    type=str)
@click.option(
    '-b',
    '--break_duration',
    default=30,
    show_default=True,
    type=int,
    help='The duration of the lunch break in minutes')
@click.option(
    '-d',
    '--workday_duration',
    default='0745',
    show_default=True,
    type=str,
    callback=validate_time_callback,
    required=True,
    help='The duration of the standard workday given in military 24h time')
def calc(ctx, workday_start, break_duration, workday_duration):
    # Validate that the workday start is in a valid time
    if not is_time_valid(workday_start):
        print(f'Start of the workday time {workday_start} is an impossible time')
        ctx.exit()

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
    help='Tags to be applied to the wokday task')
@click.option(
    '-m',
    '--message',
    default='',
    show_default=True,
    type=str,
    help='A descriptive message associated with the task')
@click.option(
    '-e',
    '--end',
    default='',
    show_default=True,
    type=str,
    callback=validate_time_callback,
    help='The time at which the work task was finished')
@click.option(
    '-d',
    '--date',
    default='',
    show_default=True,
    callback=validate_date_callback,
    type=str,
    help='The date at which the task has happened')
def start(ctx, task_start, end, tag, message, date):
    if not is_time_valid(task_start):
        print(f'Start time {task_start} of the task is an impossible time')
        ctx.exit()

    start_work_task(task_start, end, tag, message, date)


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

    data = []
    for task in tasks:
        data.append(task_to_printout(task))

    tt.print(
        data,
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


if __name__ == '__main__':
    cli(obj={})
