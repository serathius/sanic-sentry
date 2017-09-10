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

To initialize plugin using initializer:

.. code:: python
    >>> plugin = SanicSentry(app)

Or just like Flask app use `init_app` to reverse dependencies:

.. code:: python
>>> plugin = SanicSentry()
>>> SanicSentry().init_app(app)
