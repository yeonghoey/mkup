import click

from orgy.commands.mv import mv
from orgy.commands.prune import prune


@click.group()
def cli():
    pass


cli.command()(prune)
cli.command()(mv)


if __name__ == '__main__':
    cli()
