import logging

import sanic

import raven
import raven_aiohttp
from raven.handlers.logging import SentryHandler

try:
    from sanic.log import logger
except ImportError:
    logger = logging.getLogger('sanic')


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
            release=app.config.get('SENTRY_RELEASE', None)
        )
        self.handler = SentryHandler(client=self.client, level=app.config.get('SENTRY_LEVEL', logging.ERROR))
        logger.addHandler(self.handler)
        self.app = app
        self.app.sentry = self
