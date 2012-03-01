#!/usr/bin/python
"""Setup script for MrsDash."""

from setuptools import setup
from setuptools import find_packages

__version__ = '0.1.4'

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


setup(
    # long_description=__doc__,
    author='Adam Hitchcock',
    author_email='adam@disqus.com',
    description='Makes graphite dashboards easy',
    include_package_data=True,
    install_requires=install_requires,
    license='Apache License 2.0',
    name='mrsdash',
    packages=find_packages(exclude=["tests"]),
    test_suite='nose.collector',
    tests_require=tests_require,
    url='https://www.github.com/NorthIsUp/mrsdash',
    version=__version__,
    zip_safe=False,
)
