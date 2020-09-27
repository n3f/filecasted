import click
import os

from .project import get_version


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(get_version())
    ctx.exit()


@click.command()
@click.option('--version', expose_value=False, is_eager=True, callback=print_version, is_flag=True)
def run():
    click.echo('yo')
