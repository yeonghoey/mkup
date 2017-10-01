import click

from maup.commands.mv import mv
from maup.commands.prune import prune


@click.group()
def cli():
    pass


cli.command()(prune)
cli.command()(mv)


if __name__ == '__main__':
    cli()
