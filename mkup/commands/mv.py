import os

from os.path import abspath, basename, dirname, join, relpath

from click import argument, confirm, echo, option, pass_obj, Path, secho

from mkup.core import ensure_path, relfiles


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

    # Prepare 'dst'
    ensure_path(dst)
    if os.path.isdir(dst):
        dst = join(dst, basename(src))
    dst = abspath(dst)

    # Preconditions
    assert os.path.isabs(src)
    assert os.path.isabs(dst)
    if src == dst:
        return

    # Build plan
    plan = [(src, dst)]
    for src_relfile in relfiles(src, encoding):
        dst_relfile = join(dirname(dst), 
                           relpath(src_relfile, dirname(src)))
        if src_relfile != dst_relfile:
            plan.append((src_relfile, dst_relfile))

    # Print plan
    cwd = os.getcwd()
    relplan = [(relpath(s, cwd), relpath(d, cwd)) for s, d in plan]
    relsrc_len = max(len(s) for s, _ in relplan)
    reldst_len = max(len(d) for _, d in relplan)
    for s, d in relplan:
        secho('{:{width}}'.format(s, width=relsrc_len), fg='red', nl=False)
        secho(' -> ', nl=False)
        secho('{:{width}}'.format(d, width=reldst_len), fg='blue')

    # Move files
    move = yes or confirm('Move?')
    if move:
        for s, d in plan:
            ensure_path(d)
            os.rename(s, d)
