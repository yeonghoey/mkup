import os

import click
from click import echo, secho

from orgy.core import ensure_path, IMAGE_EXTENSIONS, ORG_EXTENSIONS


click.disable_unicode_literals_warning = True


@click.group()
@click.option('--encoding', default='utf8')
@click.option('--dry-run', is_flag=True, default=False)
@click.pass_context
def cli(ctx, encoding, dry_run):
    ctx.obj = {'encoding': encoding, 'dry_run': dry_run}



if __name__ == '__main__':
    cli()
