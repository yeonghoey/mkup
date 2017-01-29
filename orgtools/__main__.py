# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os

import click
from click import echo

from orgtools.links import relfiles_in_file


click.disable_unicode_literals_warning = True


SRC_PATH = click.Path(exists=True, dir_okay=False, resolve_path=True)
DST_PATH = click.Path(resolve_path=True)


@click.group()
def cli():
    pass


@cli.command()
@click.argument('src', type=SRC_PATH)
@click.option('--abspath', is_flag=True, default=False)
@click.option('--encoding', default='utf8')
def relfiles(src, abspath, encoding):
    if abspath:
        basedir, _ = os.path.split(src)
    for rel in relfiles_in_file(src, encoding):
        if abspath:
            path = os.path.join(basedir, rel)
            path = os.path.abspath(path)
        else:
            path = rel
        echo(path)


@cli.command()
@click.argument('src', type=SRC_PATH)
@click.option('--encoding', default='utf8')
def mv(src, encoding):
    print src, encoding


if __name__ == '__main__':
    cli()
