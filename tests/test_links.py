# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from orgtools.imgrefs import extract


SAMPLES = [
    '',
    '[[file.txt]]',
    '[[image.png][description]]',
    '[[http://example.com][example]] [[image.png]]',
    '''* Test
    - [[path/to/image.jpg]]
    - [[file:path/to/image.jpeg]]
    - [[http://example.com][Example]] Site.
    ** Nested
    - [[/more/image.gif][gif?]]
    - [[file:/more/image.gif][gif?]]
    ''',
]


def test_extract():
    expectations = [
        [],
        ['file.txt'],
        ['image.png'],
        ['http://example.com', 'image.png'],
        ['path/to/image.jpg', 'file:path/to/image.jpeg', 'http://example.com',
         '/more/image.gif', 'file:/more/image.gif'],
    ]
    for s, e in zip(SAMPLES, expectations):
        assert e == extract(s)
