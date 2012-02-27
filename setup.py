"""Setup script for MrsDash."""

from setuptools import setup

setup(
    name='mrsdash',
    version='1.0.0',
    description='Makes graphite dashboards easy',
    author='Adam Hitchcock',
    author_email='adam@disqus.com',
    url='https://www.github.com/NorthIsUp/mrsdash',
    package_dir={
        '': 'mrsdash'
    },
    test_suite='nose.collector',
    zip_safe=True
)
