#!/usr/bin/env python
from os import path as op

from setuptools import setup


def _read(fname):
    return open(op.join(op.dirname(__file__), fname)).read()


install_requires = [
    line for line in _read('requirements.txt').split('\n')
    if line and not line.startswith('#')]

setup(
    name='sanic-sentry',
    version='0.1.7',
    license='MIT',
    description='Sentry integration to sanic web server',
    long_description=_read('README.rst'),
    platforms=('Any'),
    keywords=['sanic', 'sentry'],

    author='Marek Siarkowicz',
    url='https://github.com/serathius/sanic-sentry',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
    ],

    py_modules=['sanic_sentry'],
    install_requires=install_requires,
)
