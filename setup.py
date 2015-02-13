"""
CachedImporter is a `finder` object that caches the directory
listings of folders on the Python path as it discovers them.

This can reduce the start-up time of scripts and applications that
import a large number of modules.

See PEP 302 (http://www.python.org/dev/peps/pep-0302/) for more info.
"""
from setuptools import setup

setup(
    name="cachedimporter",
    author="Renshaw Bay",
    description="Python import hook that caches directory listings",
    license="MIT",
    url="https://github.com/renshawbay/cachedimporter",
    version="0.1",
    py_modules=["test_import"],
    test_suite="tests"
)
