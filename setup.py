#!/usr/bin/env python
from os import path as op

from setuptools import setup


def _read(fname):
    try:
        return open(op.join(op.dirname(__file__), fname)).read()
    except IOError:
        return ''


install_requires = [
    l for l in _read('requirements.txt').split('\n')
    if l and not l.startswith('#')]

setup(
    name='sanic-sentry',
    version='0.1.3',
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
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
    ],

    py_modules=['sanic_sentry'],
    install_requires=install_requires,
)
