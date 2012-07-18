#!/usr/bin/python
"""Setup script for MrsDash."""

from setuptools import setup
from setuptools import find_packages
import fnmatch
import os


def better_glob(dir, patterns):
    matches = []
    for root, _dirnames, filenames in os.walk(dir):
        for pat in patterns:
            for filename in fnmatch.filter(filenames, pat):
                matches.append(os.path.join(root[len(dir) + 1:], filename))
    return matches

__version__ = '0.1.19'

tests_require = [
    'nose',
    'unittest2',
]

install_requires = [
    "Flask",
    "anyjson",
    "path.py",
    "disqus-flask",
    "ordereddict",  # for python 2.6
]

resources = better_glob('mrsdash', ("*.html", "*.css", "*.js", "*.ico"))

setup(
    # long_description=__doc__,
    author='Adam Hitchcock',
    author_email='adam@disqus.com',
    description='Makes graphite dashboards easy',
    include_package_data=True,
    install_requires=install_requires,
    license='Apache License 2.0',
    name='mrsdash',
    # package_data={
    #     'mrsdash': resources
    #     },
    package_dir={
        'mrsdash': 'mrsdash'
        },
    packages=find_packages(exclude=["tests"]),
    test_suite='nose.collector',
    tests_require=tests_require,
    setup_requires=[
        'setuptools-git'
        ],
    url='https://www.github.com/NorthIsUp/mrsdash',
    version=__version__,
    zip_safe=False,

)
