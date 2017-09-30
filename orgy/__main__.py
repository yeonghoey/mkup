import os

import click
from click import echo, secho

from orgy.links import relfiles_in_file
from orgy.utils import ensure_path, IMAGE_EXTENSIONS, ORG_EXTENSIONS


click.disable_unicode_literals_warning = True


SRC_PATH = click.Path(exists=True, dir_okay=False, resolve_path=True)
DST_PATH = click.Path(exists=False, dir_okay=True, resolve_path=False)
DIR_PATH = click.Path(exists=True, file_okay=False, dir_okay=True,
                      resolve_path=True)


@click.group()
@click.option('--encoding', default='utf8')
@click.option('--dry-run', is_flag=True, default=False)
@click.pass_context
def cli(ctx, encoding, dry_run):
    ctx.obj = {'encoding': encoding, 'dry_run': dry_run}


@cli.command()
@click.argument('src', type=SRC_PATH)
@click.pass_obj
def relfiles(opts, src):
    encoding = opts['encoding']
    for rel in relfiles_in_file(src, encoding):
        echo(rel)


@cli.command()
@click.argument('basedir', type=DIR_PATH)
@click.option('extensions', '--extension', '-e',
              multiple=True, default=list(IMAGE_EXTENSIONS))
@click.option('org_extensions', '--org-extension', '-o',
              multiple=True, default=list(ORG_EXTENSIONS))
@click.option('--delete', is_flag=True, default=False)
@click.pass_obj
def prune(opts, basedir, extensions, org_extensions, delete):
    encoding = opts['encoding']

    orgfiles, candidates = set(), set()
    for root, dirnames, filenames in os.walk(basedir):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            if filepath.endswith(extensions):
                candidates.add(filepath)
            if filepath.endswith(org_extensions):
                orgfiles.add(filepath)

    relfiles = set()
    for orgfile in orgfiles:
        basedir, _ = os.path.split(orgfile)
        for relfile in relfiles_in_file(orgfile, encoding):
            filepath = os.path.join(basedir, relfile)
            relfiles.add(filepath)

    targets = candidates - relfiles
    for target in targets:
        if delete:
            secho(target, fg='red')
            os.remove(target)
        else:
            echo(target)


@cli.command()
@click.argument('src', type=SRC_PATH)
@click.argument('dst', type=DST_PATH)
@click.pass_obj
def mv(opts, src, dst):
    """Move src org file to dst.

    'src' is always absolute path for an existing file, by click.
    'dst' can be any path and resolved manually.
          uses src's filename
          if 'dst' is a existing directory or endswith 'os.sep'
    """
    encoding = opts['encoding']
    dry_run = opts['dry_run']

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
