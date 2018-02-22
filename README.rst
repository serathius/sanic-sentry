Sanic-Sentry
============

Sanic-Sentry -- Sentry integration to sanic web server.


Requirements
------------

- python >= 3.5

Installation
------------

**Sanic-Sentry** should be installed using pip: ::

    pip install sanic-sentry

Usage
-----

**SENTRY_DSN**  - Sentry DSN for your application

To begin we'll set up a Sanic app:

.. code:: python

  >>> from sanic import Sanic
  >>> from sanic_sentry import SanicSentry
  >>> app = Sanic(__name__)
  >>> app.config['SENTRY_DSN'] = 'http://public:secret@example.com/1'

To initialize plugin you can pass 'app' to __init__:

.. code:: python

  >>> plugin = SanicSentry(app)

Or use `init_app` to reverse dependency:

.. code:: python

  >>> plugin = SanicSentry()
  >>> plugin.init_app(app)

``SENTRY_DSN`` is not mandatory. Here is the process :

- if ``app.config['SENTRY_DSN']`` is set, it use it
- if not it will look at envrionment variable ``SENTRY_DSN``
- finally if no ``SENTRY_DSN`` can be found, raven will not send anything to sentry.

*Optional parameters:* 

**SENTRY_PARAMS**  - Configure advanced parameters for sentry:

Explained in https://docs.sentry.io/clients/python/advanced/

.. code:: python

  >>> app.config['SENTRY_PARAMS'] = {
  ...     "release": "myapp_v0.4",
  ...     "environment": "production",
  ... }
