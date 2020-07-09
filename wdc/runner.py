import click

from .calculator import calc_workday_end


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
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
    help='The duration of the standard workday given in military 24h time')
def calc(ctx, workday_start, break_duration, workday_duration):
    wd_end = calc_workday_end(workday_start, break_duration, workday_duration)

    print(wd_end)


if __name__ == '__main__':
    cli(obj={})
