import codecs
import os
import re


LINK = re.compile(r'\[\[([^\]]+)\](?:\[[^\]]+\])?\]')
RELPATH = re.compile(r'^(?:[^/ ]+/?)+$')


def extract(content):
    return LINK.findall(content)


def relfiles(content, basedir='.'):
    for link in extract(content):
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
