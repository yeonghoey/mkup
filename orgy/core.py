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
