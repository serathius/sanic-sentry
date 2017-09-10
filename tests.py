import logging
from unittest import mock

import sanic
import sanic.response
from sanic.websocket import WebSocketProtocol

import pytest
import sanic_sentry


@pytest.yield_fixture
def app():
    app = sanic.Sanic("test_sanic_app")
    yield app


@pytest.fixture
def sanic_server(loop, app, test_server):
    return loop.run_until_complete(test_server(app))


@pytest.fixture
def client(loop, app, test_client):
    return loop.run_until_complete(test_client(app))


@pytest.fixture
def websocket_client(loop, app, test_client):
    return loop.run_until_complete(test_client(app, protocol=WebSocketProtocol))


async def test_simple(app, client):
    app.config['SENTRY_DSN'] = 'http://public:secret@example.com/1'
    plugin = sanic_sentry.SanicSentry(app)
    plugin.client.send = mock.Mock()

    @app.route('/test')
    def simple(request):
        return sanic.response.text('text')

    response = await client.get('/test')
    assert response.status == 200
    response_text = await response.text()
    assert response_text == 'text'
    assert plugin.client.send.mock_calls == []


async def test_exception(app, client):
    app.config['SENTRY_DSN'] = 'http://public:secret@example.com/1'
    plugin = sanic_sentry.SanicSentry(app)
    plugin.client.send = mock.Mock()

    @app.route('/test')
    def simple(request):
        raise Exception

    response = await client.get('/test')
    assert response.status == 500
    assert plugin.client.send.mock_calls == [mock.ANY]


async def test_warning(app, client):
    app.config['SENTRY_DSN'] = 'http://public:secret@example.com/1'
    app.config['SENTRY_LEVEL'] = logging.WARNING
    plugin = sanic_sentry.SanicSentry(app)
    plugin.client.send = mock.Mock()

    @app.route('/test')
    def simple(request):
        logging.getLogger('sanic').warning('SOMETHING bad happen')
        return sanic.response.text('text')

    response = await client.get('/test')
    assert response.status == 200
    response_text = await response.text()
    assert response_text == 'text'
    assert plugin.client.send.mock_calls == [mock.ANY]


async def test_warning_not_send(app, client):
    app.config['SENTRY_DSN'] = 'http://public:secret@example.com/1'
    plugin = sanic_sentry.SanicSentry(app)
    plugin.client.send = mock.Mock()

    @app.route('/test')
    def simple(request):
        logging.getLogger('sanic').warning('SOMETHING bad happen')
        return sanic.response.text('text')

    response = await client.get('/test')
    assert response.status == 200
    response_text = await response.text()
    assert response_text == 'text'
    assert plugin.client.send.mock_calls == []


async def test_error_handler(app, client):
    app.config['SENTRY_DSN'] = 'http://public:secret@example.com/1'
    plugin = sanic_sentry.SanicSentry(app)
    plugin.client.send = mock.Mock()

    class CustomException(Exception):
        pass

    @app.route('/test')
    def simple(request):
        raise CustomException

    @app.exception(CustomException)
    def handle_custom(request, exception):
        return sanic.response.text('text')

    response = await client.get('/test')
    assert response.status == 200
    response_text = await response.text()
    assert response_text == 'text'
    assert plugin.client.send.mock_calls == []


async def test_exception_in_error_handler(app, client):
    app.config['SENTRY_DSN'] = 'http://public:secret@example.com/1'
    plugin = sanic_sentry.SanicSentry(app)
    plugin.client.send = mock.Mock()

    class CustomException(Exception):
        pass

    @app.route('/test')
    def simple(request):
        raise CustomException

    @app.exception(CustomException)
    def handle_custom(request, exception):
        raise Exception

    response = await client.get('/test')
    assert response.status == 500
    assert plugin.client.send.mock_calls == [mock.ANY]


async def test_websocket(app, websocket_client):
    app.config['SENTRY_DSN'] = 'http://public:secret@example.com/1'
    plugin = sanic_sentry.SanicSentry(app)
    plugin.client.send = mock.Mock()

    @app.websocket('/test')
    async def simple(request, ws):
        await ws.send('text')

    ws_conn = await websocket_client.ws_connect('/test')
    msg = await ws_conn.receive()
    assert msg.data == 'text'
    await ws_conn.close()

    assert plugin.client.send.mock_calls == []


async def test_websocket_exception(app, websocket_client):
    app.config['SENTRY_DSN'] = 'http://public:secret@example.com/1'
    plugin = sanic_sentry.SanicSentry(app)
    plugin.client.send = mock.Mock()

    @app.websocket('/test')
    async def simple(request, ws):
        raise Exception

    ws_conn = await websocket_client.ws_connect('/test')
    msg = await ws_conn.receive()
    assert msg.type.value == 258
    await ws_conn.close()

    assert plugin.client.send.mock_calls == [mock.ANY]
