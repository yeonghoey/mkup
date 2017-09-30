from click import argument, echo, option, Path, secho


@argument('basedir',
          type=Path(exists=True,
                    file_okay=False,
                    dir_okay=True,
                    resolve_path=True))

@option('org_extensions', '--org-extension', '-o',
        multiple=True,
        default=['.org', '.org_archive'])

@option('rel_extensions', '--rel-extension', '-r',
        multiple=True,
        default=['.png', '.jpg', '.jpeg', '.gif'])

@option('encodig', '--encoding',
        default='utf8')

@option('dry_run', '--dry-run',
        is_flag=True,
        default=False)

def prune(basedir,
          org_extensions,
          rel_extensions,
          encoding,
          dry_run):

    files = collect_files(basedir, {
        'org': org_extensions,
        'rel': rel_extensions
    })

    existing = sum(relfilelink_paths(p) for p in files['org'])
    targets = files['rel'] - existing
    for target in targets:
        echo(target)
        # if delete:
        #     secho(target, fg='red')
        #     os.remove(target)
        # else:
