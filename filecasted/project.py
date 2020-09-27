"""
import addict
import pathlib
import toml


def load_config():
    config = None
    file = pathlib.Path(__file__) / '../../pyproject.toml'
    file = file.resolve()
    with file.open() as f:
        config = toml.load(f)
    return addict.Dict(config)


def get_version():
    ""Get the project version from the poetry file""
    config = load_config()
    return f'{config.tool.poetry.name}: {config.tool.poetry.version}'
"""