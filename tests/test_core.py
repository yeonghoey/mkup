import os

from mkup.core import collect_files, extract_links, select_filelinks


SAMPLES = [
    '',

    '[[file.txt]]',

    '[[image.png][description]]',

    '[[file:image.png]]',

    '[[http://example.com][example]] [[image.png]]',

    '''* Test
    - [[path/to/image.jpg]]
    - [[file:path/to/image.jpeg]]
    - [[http://example.com][Example]] Site.
    ** Nested
    - [[/more/image.gif][gif?]]
    - [[irc:/irc.com][gif?]]
    - [[file:/more/image.gif][gif?]]
    - [[#internal]]
    ''',
]


def assert_samples(f, expectations):
    for s, e in zip(SAMPLES, expectations):
        assert list(f(s)) == e


def test_ensure_path():
    pass


def test_collect_files(tmpdir):
    basedir = tmpdir.mkdir('yeonghoey')

    basedir.join('foo.org').write('')
    basedir.join('bar.png').write('')
    basedir.join('baz.jpg').write('')
    basedir.join('qux.txt').write('')
    basedir.join('xxx.yyy').write('')

    files = collect_files(basedir, {
        'org': ['.org'],
        'img': ['.png', '.jpg'],
        'xxx': ['.org', '.txt'],
    })

    assert files == {
        'org': set([basedir.join('foo.org')]),
        'img': set([basedir.join('bar.png'),
                    basedir.join('baz.jpg')]),
        'xxx': set([basedir.join('foo.org'),
                    basedir.join('qux.txt')]),
    }


def test_refilelink_paths():
    pass


def test_select_filelinks():

    def extract_filelinks(content):
        links = extract_links(content)
        return select_filelinks(links)

    assert_samples(extract_filelinks, [
        [],

        ['file.txt'],

        ['image.png'],

        ['file:image.png'],

        ['image.png'],

        ['path/to/image.jpg',
         'file:path/to/image.jpeg',
         '/more/image.gif',
         'file:/more/image.gif']
    ])


def test_extract_links():
    assert_samples(extract_links, [
        [],

        ['file.txt'],

        ['image.png'],

        ['file:image.png'],

        ['http://example.com', 'image.png'],

        ['path/to/image.jpg',
         'file:path/to/image.jpeg',
         'http://example.com',
         '/more/image.gif',
         'irc:/irc.com',
         'file:/more/image.gif',
         '#internal'],
    ])
