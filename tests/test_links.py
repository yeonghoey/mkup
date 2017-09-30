import os

from orgy.links import extract, relfiles


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
    - [[#internal]]
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
         '/more/image.gif', 'file:/more/image.gif', '#internal'],
    ])


def test_relfiles(monkeypatch):
    def mock_exists(path):
        """Distinguish internal links from files"""
        _, name = os.path.split(path)
        return not name.startswith('#')

    monkeypatch.setattr(os.path, 'exists', mock_exists)
    assert_samples(relfiles, [
        [],
        ['file.txt'],
        ['image.png'],
        ['image.png'],
        ['path/to/image.jpg', 'path/to/image.jpeg']
    ])
