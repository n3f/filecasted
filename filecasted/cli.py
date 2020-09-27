import click
import pathlib

from .project import get_version


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(get_version())
    ctx.exit()


def validate_output(ctx, param, value):
    output = pathlib.Path(value).resolve()
    if (output.exists() and (
            ctx.params.get('force', False) is not True or
            ctx.params.get('append', False) is not True)):
        raise click.BadParameter('file exists')


@click.command()
@click.option('--version', expose_value=False, is_eager=True, callback=print_version, is_flag=True)
@click.option('-f', '--force', is_flag=True, is_eager=True, help='Force the output to an existing file.')
@click.option('-a', '--append', is_flag=True, is_eager=True, help='Append INPUT to the output file.')
@click.option('-o', '--output', nargs=1, type=click.Path(exists=False, writable=True, allow_dash=True),
              default='./rss.xml', callback=validate_output)
@click.argument('_input', nargs=-1, type=click.Path(exists=True, readable=True, allow_dash=True), metavar='INPUT')
def run(**kwargs):
    """
    Create a podcast file from INPUT.

    INPUT can be a playlist (`.m3u`), stdin (`-`), or a collection of audio files.  Playlists and stdin should
    be a simple text document with a list of files to add.
    """
    click.echo(f'{kwargs.get("_input")}:{kwargs.get("output")}')

