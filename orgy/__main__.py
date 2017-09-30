import click


@click.group()
def cli():
    pass


@cli.command
def foo():
    print('foo')


if __name__ == '__main__':
    cli()
