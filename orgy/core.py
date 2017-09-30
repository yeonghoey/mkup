import codecs
import os
import re


RELPATH = re.compile(r'^(?:[^/ ]+/?)+$')


def collect_files(basedir, exts):
    for root, _, filenames in os.walk(basedir):
        for fn in filenames:
            p = os.path.join(root, fn)
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


def extract_links(content):
    # '[[link][description]]' or '[[link]]'
    return re.findall(r'\[\[([^\]]+)\](?:\[[^\]]+\])?\]', content)


def relfiles(links, basedir):
    for path in links:
        link = link[5:] if link.startswith('file:') else link
        m = RELPATH.match(link)
        if m is not None:
            rel = m.group(0)
            path = os.path.join(basedir, m.group(0))
            path = os.path.abspath(path)
            if os.path.exists(path):
                yield rel


def relfiles_in_file(path, encoding='utf8'):
    with codecs.open(path, 'r', encoding=encoding) as f:
        content = f.read()
    basedir, _ = os.path.split(path)
    return relfiles(content, basedir)
