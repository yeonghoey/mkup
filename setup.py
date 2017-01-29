"""
orgtools streamlines managing org documents
"""
from setuptools import setup, find_packages


setup(
    name='orgtools',
    version='0.0.1',
    description=__doc__,
    author='Yeongho Kim',
    author_email='yeonghoey@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords='productivity',
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
            'org=orgtools.__main__:cli',
        ]
    },
)
