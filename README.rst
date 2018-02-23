Sanic-Sentry
============

Sanic-Sentry -- Sentry integration to sanic web server.

.. image:: https://badge.fury.io/py/sanic-sentry.svg
    :target: https://badge.fury.io/py/sanic-sentry

.. image:: https://travis-ci.org/serathius/sanic-sentry.svg?branch=master
    :target: https://travis-ci.org/serathius/sanic-sentry``

.. image:: https://codecov.io/gh/serathius/sanic-sentry/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/serathius/sanic-sentry

Requirements
------------

- python >= 3.5

Installation
------------

**Sanic-Sentry** should be installed using pip: ::

    pip install sanic-sentry

Usage
-----


To initialize plugin you can pass 'app' to __init__:

.. code:: python

  >>> from sanic import Sanic
  >>> from sanic_sentry import SanicSentry
  >>> app = Sanic(__name__)
  >>> plugin = SanicSentry(app)

Or use `init_app` to reverse dependency:

.. code:: python

  >>> plugin = SanicSentry()
  >>> plugin.init_app(app)

*Optional parameters:*

**SENTRY_DSN**  - Sentry DSN for your application:

If not set raven will fallback to SENTRY_DSN environment variable. Not setting either will disable raven.

.. code:: python

  >>> app.config['SENTRY_DSN'] = 'http://public:secret@example.com/1'

**SENTRY_PARAMS**  - Configure advanced parameters for sentry:

Explained in https://docs.sentry.io/clients/python/advanced/

.. code:: python

  >>> app.config['SENTRY_PARAMS'] = {
  ...     "release": "myapp_v0.4",
  ...     "environment": "production",
  ... }
