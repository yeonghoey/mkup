from click import argument, echo, option, pass_obj, Path, secho


@argument('src', type= Path(exists=True,
                            dir_okay=False,
                            resolve_path=True))

@argument('dst', type=Path(exists=False,
                            dir_okay=True,
                            resolve_path=False))
@pass_obj
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
