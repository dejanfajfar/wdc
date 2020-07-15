import click

from wdc.time import is_time_valid
from wdc.calculator import calc_workday_end
from wdc.controller.work_day import append_line


def validate_time_callback(ctx, param, value):
    # print(f'{param.name} = {value}')
    if is_time_valid(value):
        return value
    else:
        raise click.BadParameter(f'{value} is not a valid time')


@click.group()
@click.option('--debug/--no-debug', default=False)
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
    help='The duration of the standard workday given in military 24h time')
def calc(ctx, workday_start, break_duration, workday_duration):
    # Validate that the workday start is in a valid time
    if not is_time_valid(workday_start):
        print(f'Start of the workday time {workday_start} is an impossible time')

    wd_end = calc_workday_end(workday_start, break_duration, workday_duration)

    print(wd_end)


@cli.command()
@click.pass_context
@click.argument(
    'task_start',
    type=str,
    required=False)
def start(ctx, task_start, tags, message):
    pass


if __name__ == '__main__':
    cli(obj={})
