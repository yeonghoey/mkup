import os

from os.path import basename, dirname, join, relpath

from click import argument, echo, option, pass_obj, Path, secho

from orgy.core import ensure_path, relfilelink_paths


@argument('src',
          type= Path(exists=True,
                     dir_okay=False,
                     resolve_path=True))

@argument('dst',
          type=Path(exists=False,
                    dir_okay=True,
                    resolve_path=False))

@option('encoding', '--encoding',
        default='utf8')

@option('yes', '--yes', '-y',
        is_flag=True,
        default=False)

def mv(src,
       dst,
       encoding,
       yes):
    """Moves 'src' org file to 'dst'.

    'src' is always an absolute path for an existing file, by click.
    'dst' can be any path and resolved manually.
    it uses the 'basename(src)' if 'dst' is a directory.
    """

    ensure_path(dst)
    if os.path.isdir(dst):
        dst = os.path.join(dst, basename(src))

    dst = os.path.abspath(dst)
    srcdir = os.path.dirname(src)
    dstdir = os.path.dirname(dst)

    # target's relfiles
    for srcpath in relfilelink_paths(src, encoding):
        relpath = relpath(path, start=dirname(src))
        dstpath = join(dirname(dst), relpath)
        echo('%s -> %s' % (srcpath, dstpath))
        # if not dry_run:
        #     ensure_path(dpath)
        #     os.rename(spath, dpath)

    # Move target itself
    echo('%s -> %s' % (src, dst))
    # if not dry_run:
    #     ensure_path(dst)
        # os.rename(src, dst)
