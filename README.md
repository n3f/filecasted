# Filecasted

Create or modify podcast xml files using local files (i.e. `m3u`, `mp3`, `mp4`, etc.)

## Usage

Consists of several commands (`create`, `edit`). Use the `--help` option for additional information.

`$ filecast create --help`

```shell
Usage: filecast [OPTIONS] INPUT

  Create a podcast file from INPUT.

  INPUT can be a playlist (`.m3u`), stdin (`-`), or a collection of audio
  files.  Playlists and stdin should be a simple text document with a list
  of files to add.

Options:
  --version
  -f, --force        Force the output to an existing file.
  -a, --append       Append INPUT to the output file.
  -o, --output PATH
  --help             Show this message and exit.
```

## Examples

Create a podcast from a directory of audio files.

`$ filecast create`