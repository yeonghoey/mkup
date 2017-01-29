# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from orgtools.imgrefs import extract


def test_extract():
    assert extract('') == []
    assert extract('[[file.txt]]') == ['file.txt']
    assert extract('[[image.png][description]]') == ['image.png']
    assert extract('''
        [[http://example.org][example]]
        [[image.png]]
        ''') == ['http://example.org', 'image.png']
