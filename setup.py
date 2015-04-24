"""
CachedImporter is a `finder` object that caches the directory
listings of folders on the Python path as it discovers them.

This can reduce the start-up time of scripts and applications that
import a large number of modules.

See PEP 302 (http://www.python.org/dev/peps/pep-0302/) for more info.
"""
from setuptools import setup, find_packages

setup(
    name="cachedimporter",
    description="Python import hook that caches directory listings",
    packages=find_packages(),
    py_modules=["cachedimporter"],
    version="0.1.1",
    test_suite="nose.collector",
    tests_require=["nose>=1.2.1"],
    author="Renshaw Bay",
    author_email="technology@renshawbay.com",
    license="MIT",
    url="https://github.com/renshawbay/cachedimporter",
    classifiers=["License :: OSI Approved :: MIT License"],
)
