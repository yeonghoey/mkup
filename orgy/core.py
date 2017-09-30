import codecs
from collections import defaultdict
import os
from os.path import abspath, join, splitext
import re


def ensure_path(path):
    if path.endswith(os.sep):
        basedir = path
    else:
        basedir, _ = os.path.split(path)
    try:
        os.makedirs(basedir)
    except OSError:
        if not os.path.isdir(basedir):
            raise


def collect_files(basedir, extensions):
    # Build inverse lookup dict
    ext_kinds = defaultdict(set)
    for kind, exts in extensions.items():
        for ext in exts:
            ext_kinds[ext].add(kind)

    files = defaultdict(set)
    for root, _, filenames in os.walk(basedir):
        for fn in filenames:
            _, ext = splitext(fn)
            kinds = ext_kinds.get(ext, [])
            for k in kinds:
                abspath = join(root, fn)
                files[k].add(abspath)

    return files


def relfilelink_paths(org_path, encoding):
    with codecs.open(org_path, 'r', encoding=encoding) as f:
        content = f.read()

    basedir, _ = os.path.split(org_path)
    links = extract_links(content)
    filelinks = select_filelinks(links)

    for link in filelinks:
        # Remove 'file:' if existing
        path = re.sub(r'^file:', '', link)

        # Pick only relative paths relative
        if os.path.isabs(path):
            continue

        path = abspath(join(basedir, path))
        if os.path.exists(path):
            yield path


def select_filelinks(links):
    for link in links:
        # Skip org internal link
        if link.startswith('#'):
            continue

        # if scheme is specified, it should be 'file'
        m = re.match(r'^(?P<scheme>[^:]+)\:.+$', link)
        if m is not None and m['scheme'] != 'file':
            continue

        yield link


def extract_links(content):
    # '[[link][description]]' or '[[link]]' -> 'link'
    return re.findall(r'\[\[([^\]]+)\](?:\[[^\]]+\])?\]', content)
