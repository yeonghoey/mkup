import codecs
import os
from os.path import abspath, join
import re


def collect_files(basedir, exts):
    for root, _, filenames in os.walk(basedir):
        for fn in filenames:
            p = join(root, fn)
            if p.endswith(org_extensions):
                orgfiles.add(p)
            if p.endswith(rel_extensions):
                relfiles.add(p)
    return orgfiles, relfiles


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


def rellink_paths(org_path, encoding):
    with codecs.open(org_path, 'r', encoding=encoding) as f:
        content = f.read()

    basedir, _ = os.path.split(org_path)
    links = extract_links(content)
    relpaths = select_relpaths(links)

    for relpath in relpaths:
        path = abspath(join(basedir, relpath))
        if os.path.exists(path):
            yield path


def select_relpaths(links):
    for link in extract_links(content):
        # Match links of relpaths like:
        # - 'file:img/*'
        # - 'img/*'
        m = re.match(r'^(?:file\:)?((?:[^/ ]+/?)+)$', link)
        if m is not None:
            yield m.group(1)


def extract_links(content):
    # '[[link][description]]' or '[[link]]' -> 'link'
    return re.findall(r'\[\[([^\]]+)\](?:\[[^\]]+\])?\]', content)
