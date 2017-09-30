from itertools import chain
import os

from click import argument, confirm, echo, option, Path, secho

from orgy.core import collect_files, relfiles

@argument('directory',
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

@option('encoding', '--encoding',
        default='utf8')

@option('yes', '--yes', '-y',
        is_flag=True,
        default=False)

def prune(directory,
          org_extensions,
          rel_extensions,
          encoding,
          yes):

    files = collect_files(directory, {
        'org': org_extensions,
        'rel': rel_extensions
    })

    paths = [relfiles(p, encoding) for p in files['org']]
    existing = set(chain.from_iterable(paths))
    targets = files['rel'] - existing

    for t in targets:
        secho(t, fg='red')

    if targets:
        delete = yes or confirm('Delete?')
        if delete:
            for t in targets:
                os.remove(t)
