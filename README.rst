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

*Optional parameters:* 

**SENTRY_RELEASE**  - Configure a custom release for sentry
Explained in https://docs.sentry.io/learn/releases/

.. code:: python
>>> app.config['SENTRY_RELEASE'] = 'myapp_v0.4'


