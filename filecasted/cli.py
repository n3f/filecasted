import click

from pathlib import Path
from dataclasses import fields
from . import __version__, parse_input
from .feedgen import Feedgen


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(f'{__package__}: {__version__}')
    ctx.exit()


def validate_input(ctx, param, paths):
    """
    Verify the input args (these are the files to process)

    :param ctx:
    :param param:
    :param paths:
    :return:
    """
    # If no input provided try the current directory
    if len(paths) == 0:
        paths = '.',

    try:
        audio_extensions = ctx.params['audio_extensions'].split(',')
        # preserve ordering, but remove duplicates
        dedup = dict.fromkeys(p for p in parse_input(paths) if p.suffix in audio_extensions and p.exists())
        if len(dedup) < 1:
            raise click.BadParameter('No files found')
        return list(dedup.keys())
    except Exception as e:
        raise click.BadParameter('Unable to parse INPUT: ' + str(e))


def validate_output(ctx, param, value):
    output = Path(value).resolve()
    # click.echo(f'{ctx.params}')
    if (output.exists()
            and ctx.params.get('force', False) is not True
            and ctx.params.get('append', False) is not True):
        raise click.BadParameter('file exists')
    return output


@click.command()
@click.option('--version', expose_value=False, is_eager=True, callback=print_version, is_flag=True)
@click.option('-v', '--verbose', count=True)
@click.option('-f', '--force', is_flag=True, is_eager=True, help='Force the output to an existing file.')
@click.option('--audio-extensions', is_eager=True, help='Comma separated list of processable extensions.',
              default='.mp3,.mp4,.wav', show_default=True, metavar='EXT')
@click.option('-a', '--append', is_flag=True, is_eager=True, help='Append INPUT to the output file.')
@click.option('-o', '--output', nargs=1, type=click.Path(exists=False, writable=True, allow_dash=True),
              default='./rss.xml', callback=validate_output)
@click.option('-n', '--dry-run', is_flag=True, help="Run as normally, but don't make any permanent changes")
@click.argument('_input', nargs=-1, type=click.Path(exists=True, readable=True, allow_dash=True),
                metavar='INPUT', callback=validate_input)
def run(**kwargs):
    """
    Create a podcast file from INPUT.

    INPUT can be a playlist (`.m3u`), stdin (`-`), a directory or a collection of audio files.  Playlists and
    stdin should be a simple text document with a list of files to add.
    """

    # The following allows me to add options and pass them through to the Feedgen object without making
    # additional modifications to this function.
    feedgen_fields = tuple(f.name for f in fields(Feedgen))
    feedgen_args = {k: v for (k, v) in kwargs.items() if k in feedgen_fields}
    f = Feedgen(**feedgen_args)
    if kwargs.get('dry_run'):
        click.echo(str(f))
    else:
        f.create()
