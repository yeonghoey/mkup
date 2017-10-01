import ast
import re
from setuptools import find_packages, setup



def extract_version(content):
    m = re.search(r'__version__\s+=\s+(.*)', content)
    s = m.group(1)
    return str(ast.literal_eval(s))


with open('mkup/__init__.py', 'rb') as f:
    content = f.read().decode('utf-8')
    version = extract_version(content)


setup(
    name='mkup',
    version=version,
    description='CLI for Markups',
    keywords='cli markup markdown org',
    url='https://github.com/yeonghoey/mkup',

    author='Yeongho Kim',
    author_email='yeonghoey@gmail.com',

    packages=find_packages(),

    entry_points={
        'console_scripts': [
            'mkup=mkup.__main__:cli',
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
