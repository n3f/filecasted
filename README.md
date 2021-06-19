# Filecasted

Create or modify podcast xml files using local files (i.e. `m3u`, `mp3`, `mp4`, etc.)

## Usage

```txt
Usage: filecast [OPTIONS] INPUT

  Create a podcast file from INPUT.

  INPUT can be a playlist (`.m3u`), stdin (`-`), a directory or a collection
  of audio files.  Playlists and stdin should be a simple text document with
  a list of files to add.

Options:
  --version
  -v, --verbose
  -f, --force             Force the output to an existing file.
  --audio-extensions EXT  Comma separated list of processable extensions.
                          [default: .mp3,.mp4,.wav]

  -a, --append            Append INPUT to the output file.
  -o, --output PATH
  -n, --dry-run           Run as normally, but don't make any permanent
                          changes

  --help                  Show this message and exit.
```
