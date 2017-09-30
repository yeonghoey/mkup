from setuptools import setup



def extract_version(init_content):
    m = re.search(r'__version__\s+=\s+(.*)', content)
    s = m.group(1)
    return str(ast.literal_eval(s))


with open('orgy/__init__.py', 'rb') as f:
    init_content = f.read().decode('utf-8')
    version = extract_version(init_content)


setup(
    name='orgy',
    version=version,
    description='Orgy streamlines managing Emacs org-mode documents',

    author='Yeongho Kim',
    author_email='yeonghoey@gmail.com',

    packages=['orgy'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],

    entry_points={
        'console_scripts': [
            'orgy=orgy.__main__:cli',
        ]
    },
)
