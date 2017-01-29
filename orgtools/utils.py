# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os


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
