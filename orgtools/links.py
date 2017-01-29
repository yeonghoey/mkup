# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re


LINK = re.compile(r'\[  \[([^\]]+)\]  (?:\[[^\]]+\])?  \]', re.VERBOSE)
RELPATH = re.compile(r'^(?:[^/ ]+/?)+$')


def extract(content):
    return LINK.findall(content)


def relfiles(content):
    for link in extract(content):
        link = link[5:] if link.startswith('file:') else link
        m = RELPATH.match(link)
        if m is not None:
            yield m.group(0)
