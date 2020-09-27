import sys
from pathlib import Path

__version__ = '0.0.1'


def parse_input(paths):
    """
    Take input paths and turn into list of audio files to process.

    This is primarily just path munging and the validation will occur elsewhere.
    """
    for path in paths:
        original_path = Path(path.strip()).resolve()
        if path == '-': # stdin
            yield from [Path(line.strip()).resolve() for line in sys.stdin.readlines()]
        elif original_path.suffix == '.m3u': # playlists
            with open(path, 'r') as handle:
                yield from [original_path.with_name(f.strip()).resolve() for f in handle.readlines()]
        elif original_path.is_dir(): # directories
            yield from sorted(original_path.iterdir())
        else:  # all other files
            yield original_path
