from click import argument, echo, option, pass_obj, Path, secho


@argument('basedir', type=Path(exists=True,
                                file_okay=False,
                                dir_okay=True,
                                resolve_path=True))

@option('org_exts', '--org-ext', '-o',
            multiple=True,
            default=['.org', '.org_archive'])

@option('rel_exts', '--rel-ext', '-r',
            multiple=True,
            default=['.png', '.jpg', '.jpeg', '.gif'])

@pass_obj
def prune(opts, basedir, rel_exts, org_exts):
    encoding = opts['encoding']
    dry_run = opts['dry_run']

    files = collect_files(basedir, {'org': org_exts, 'rel': rel_exts})

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
