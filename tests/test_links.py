# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from orgtools.links import extract, relfiles


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


def assert_samples(f, expectations):
    for s, e in zip(SAMPLES, expectations):
        assert list(f(s)) == e


def test_extract():
    assert_samples(extract, [
        [],
        ['file.txt'],
        ['image.png'],
        ['http://example.com', 'image.png'],
        ['path/to/image.jpg', 'file:path/to/image.jpeg', 'http://example.com',
         '/more/image.gif', 'file:/more/image.gif'],
    ])


def test_relfiles():
    assert_samples(relfiles, [
        [],
        ['file.txt'],
        ['image.png'],
        ['image.png'],
        ['path/to/image.jpg', 'path/to/image.jpeg'] 
    ])
