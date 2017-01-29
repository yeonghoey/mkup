# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os

import click
from click import echo

from orgtools.links import relfiles_in_file
from orgtools.utils import ensure_path


click.disable_unicode_literals_warning = True


SRC_PATH = click.Path(exists=True, dir_okay=False, resolve_path=True)
DST_PATH = click.Path(exists=False, dir_okay=True, resolve_path=False)


@click.group()
def cli():
    pass


@cli.command()
@click.argument('src', type=SRC_PATH)
@click.option('--encoding', default='utf8')
@click.option('--abspath', is_flag=True, default=False)
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
@click.argument('dst', type=DST_PATH)
@click.option('--encoding', default='utf8')
@click.option('--dry-run', is_flag=True, default=False)
def mv(src, dst, encoding,dry_run):
    """Move src org file to dst.

    'src' is always absolute path for an existing file, by click.
    'dst' can be any path and resolved manually.
          uses src's filename
          if 'dst' is a existing directory or endswith 'os.sep'
    """
    if os.path.isdir(dst) or dst.endswith(os.sep):
        _, src_name = os.path.split(src)
        dst = os.path.join(dst, src_name)

    dst = os.path.abspath(dst)
    src_basedir, _ = os.path.split(src)
    dst_basedir, _ = os.path.split(dst)

    if not os.path.exists(dst_basedir):
        os.makedirs(dst_basedir)

    # Move target's relfiles
    for rel in relfiles_in_file(src, encoding):
        spath = os.path.join(src_basedir, rel)
        dpath = os.path.join(dst_basedir, rel)
        echo('%s -> %s' % (spath, dpath))
        if not dry_run:
            ensure_path(dpath)
            os.rename(spath, dpath)

    # Move target itself
    echo('%s -> %s' % (src, dst))
    if not dry_run:
        ensure_path(dst)
        os.rename(src, dst)


if __name__ == '__main__':
    cli()
