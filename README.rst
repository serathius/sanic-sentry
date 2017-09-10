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

The plugin starts working automaticaly, but you can use it manually:

.. code:: python

    from sanic import Sanic
    from sanic_sentry import SanicSentry

    app = Sanic(__name__)
    app.config['SENTRY_DSN'] = 'http://public:secret@example.com/1'

    SanicSentry.init_app(app)

