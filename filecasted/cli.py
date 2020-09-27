import click
import pathlib
import sys

from . import __version__


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(f'{__package__}: {__version__}')
    ctx.exit()


def get_paths(path):
    if path == '-':
        return sys.stdin.readlines()
    elif pathlib.Path(path).suffix() == '.m3u':
        with open(path, 'r') as handle:
            return handle.readlines()
    raise click.BadParameter(f'{path} must be stdin (-) or a .m3u file.')


def validate_input(ctx, param, paths):
    if len(paths) == 1:
        paths = get_paths(paths[0])

    audio_extensions = ctx.params['audio_extensions'].split(',')
    for path_name in paths:
        path = pathlib.Path(path_name).resolve()
        ext = path.suffix
        if not path.resolve().exists() or ext not in audio_extensions:
            raise click.BadParameter(f'{path_name.strip()} not an audio file')
    raise click.BadParameter('unable to validate')


def validate_output(ctx, param, value):
    output = pathlib.Path(value).resolve()
    if (output.exists() and (
            ctx.params.get('force', False) is not True or
            ctx.params.get('append', False) is not True)):
        raise click.BadParameter('file exists')


@click.command()
@click.option('--version', expose_value=False, is_eager=True, callback=print_version, is_flag=True)
@click.option('-f', '--force', is_flag=True, is_eager=True, help='Force the output to an existing file.')
@click.option('--audio-extensions', is_eager=True, help='Comma separated list of processable extensions.',
              default='.mp3,.mp4,.wav')
@click.option('-a', '--append', is_flag=True, is_eager=True, help='Append INPUT to the output file.')
@click.option('-o', '--output', nargs=1, type=click.Path(exists=False, writable=True, allow_dash=True),
              default='./rss.xml', callback=validate_output)
@click.argument('_input', nargs=-1, type=click.Path(exists=True, readable=True, allow_dash=True),
                metavar='INPUT', callback=validate_input)
def run(**kwargs):
    """
    Create a podcast file from INPUT.

    INPUT can be a playlist (`.m3u`), stdin (`-`), or a collection of audio files.  Playlists and stdin should
    be a simple text document with a list of files to add.
    """
    click.echo(f'{kwargs.get("_input")}:{kwargs.get("output")}')

