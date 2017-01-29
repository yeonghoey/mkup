# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

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
            path = os.path.join(basedir, m.group(0))
            path = os.path.abspath(path)
            if os.path.exists(path):
                yield path
