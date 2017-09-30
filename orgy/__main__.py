import os

import click
from click import echo, secho

from orgy.core import ensure_path, IMAGE_EXTENSIONS, ORG_EXTENSIONS


@click.group()
def cli(ctx):
    pass


if __name__ == '__main__':
    cli()
