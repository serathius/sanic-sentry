import logging

import sanic

import raven
import raven_aiohttp
from raven.handlers.logging import SentryHandler


class SanicSentry:
    def __init__(self, app=None):
        self.app = None
        self.handler = None
        self.client = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app: sanic.Sanic):
        self.client = raven.Client(
            dsn=app.config['SENTRY_DSN'],
            transport=raven_aiohttp.AioHttpTransport,
        )
        self.handler = SentryHandler(client=self.client, level=app.config.get('SENTRY_LEVEL', logging.ERROR))
        logger = logging.getLogger('sanic')
        logger.addHandler(self.handler)
        self.app = app
        self.app.sentry = self
