# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re


LINK_PATTERN = re.compile(r'\[  \[([^\]]+)\]  (?:\[[^\]]+\])?  \]', re.VERBOSE)


def extract(content):
    return LINK_PATTERN.findall(content)
