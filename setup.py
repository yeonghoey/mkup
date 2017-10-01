import ast
import re
from setuptools import setup



def extract_version(content):
    m = re.search(r'__version__\s+=\s+(.*)', content)
    s = m.group(1)
    return str(ast.literal_eval(s))


with open('maup/__init__.py', 'rb') as f:
    content = f.read().decode('utf-8')
    version = extract_version(content)


setup(
    name='maup',
    version=version,
    description='CLI for MArkUP files',

    author='Yeongho Kim',
    author_email='yeonghoey@gmail.com',

    packages=['maup'],

    entry_points={
        'console_scripts': [
            'maup=maup.__main__:cli',
        ]
    },

    install_requires=[
        'click>=6.7'
    ],

    classifiers=[
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.6',
    ],

)
