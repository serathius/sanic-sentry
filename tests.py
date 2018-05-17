import asyncio
import json
import logging
import threading
import zlib

import sanic
import sanic.response
from sanic.websocket import WebSocketProtocol

import flask
import pytest
import sanic_sentry
from werkzeug.routing import PathConverter
from werkzeug.serving import make_server


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


@pytest.fixture
def mock_service():
    with Service(host='127.0.0.1', port=8000) as service:
        yield service


@pytest.fixture
def sentry_calls():
    return []


@pytest.fixture
def sentry_url(sentry_mock):
    return 'http://public:secret@127.0.0.1:8000/1'


@pytest.fixture
def sentry_mock(mock_service, sentry_calls):

    @mock_service.app.route('/<everything:path>', methods=['POST'])
    def handle_request(path):
        sentry_calls.append((path, flask.request.mimetype,
                             json.loads(zlib.decompress(flask.request.data).decode('utf-8'))))
        return ''

    return mock_service


async def test_simple(app, client, sentry_url, sentry_calls):
    app.config['SENTRY_DSN'] = sentry_url
    sanic_sentry.SanicSentry(app)

    @app.route('/test')
    def simple(request):
        return sanic.response.text('text')

    response = await client.get('/test')
    assert response.status == 200
    response_text = await response.text()
    assert response_text == 'text'
    await asyncio.sleep(0.01)
    assert len(sentry_calls) == 0


@pytest.mark.parametrize('params', [
    None,
    {},
    {'release': None},
    {'release': 'myapp_v0.4'},
])
async def test_exception(app, client, sentry_calls, sentry_url, params):
    app.config['SENTRY_DSN'] = sentry_url
    if params is not None:
        app.config['SENTRY_PARAMS'] = params
    sanic_sentry.SanicSentry(app)

    @app.route('/test')
    def simple(request):
        raise Exception

    response = await client.get('/test')
    assert response.status == 500

    await asyncio.sleep(0.01)
    assert len(sentry_calls) == 1
    assert sentry_calls[0][0] == 'api/1/store/'
    assert sentry_calls[0][1] == 'application/octet-stream'
    assert sentry_calls[0][2]['level'] == 40
    assert sentry_calls[0][2]['tags'] == {}
    assert sentry_calls[0][2]['project'] == '1'
    assert sentry_calls[0][2]['repos'] == {}
    if params and params.get('release'):
        assert sentry_calls[0][2]['release'] == params.get('release')
    else:
        assert 'release' not in sentry_calls[0][2]
    assert set(sentry_calls[0][2]['extra'].keys()) == {'sys.argv', 'pathname', 'filename', 'stack_info', 'lineno',
                                                       'thread', 'threadName', 'processName', 'process', 'asctime'}
    assert len(sentry_calls[0][2]['breadcrumbs']['values']) == 1
    assert sentry_calls[0][2]['breadcrumbs']['values'][0]['data'] == {}
    assert 'python' in sentry_calls[0][2]['modules']


async def test_warning(app, client, sentry_calls, sentry_url):
    app.config['SENTRY_DSN'] = sentry_url
    app.config['SENTRY_LEVEL'] = logging.WARNING
    sanic_sentry.SanicSentry(app)

    @app.route('/test')
    def simple(request):
        try:
            from sanic.log import logger
        except ImportError:
            logger = logging.getLogger('sanic')
        logger.warning('SOMETHING bad happen')
        return sanic.response.text('text')

    response = await client.get('/test')
    assert response.status == 200
    response_text = await response.text()
    assert response_text == 'text'

    await asyncio.sleep(0.01)
    assert len(sentry_calls) == 1
    assert sentry_calls[0][2]['level'] == 30


async def test_warning_not_sent(app, client, sentry_calls, sentry_url):
    app.config['SENTRY_DSN'] = sentry_url
    sanic_sentry.SanicSentry(app)

    @app.route('/test')
    def simple(request):
        logging.getLogger('sanic').warning('SOMETHING bad happen')
        return sanic.response.text('text')

    response = await client.get('/test')
    assert response.status == 200
    response_text = await response.text()
    assert response_text == 'text'

    await asyncio.sleep(0.01)
    assert len(sentry_calls) == 0


async def test_error_handler(app, client, sentry_calls, sentry_url):
    app.config['SENTRY_DSN'] = sentry_url
    sanic_sentry.SanicSentry(app)

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

    await asyncio.sleep(0.01)
    assert len(sentry_calls) == 0


async def test_exception_in_error_handler(app, client, sentry_calls, sentry_url):
    app.config['SENTRY_DSN'] = sentry_url
    sanic_sentry.SanicSentry(app)

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

    await asyncio.sleep(0.01)
    assert len(sentry_calls) == 1


async def test_websocket(app, websocket_client, sentry_calls, sentry_url):
    app.config['SENTRY_DSN'] = sentry_url
    sanic_sentry.SanicSentry(app)

    @app.websocket('/test')
    async def simple(request, ws):
        await ws.send('text')

    ws_conn = await websocket_client.ws_connect('/test')
    msg = await ws_conn.receive()
    assert msg.data == 'text'
    await ws_conn.close()

    await asyncio.sleep(0.01)
    assert len(sentry_calls) == 0


async def test_websocket_exception(app, websocket_client, sentry_calls, sentry_url):
    app.config['SENTRY_DSN'] = sentry_url
    sanic_sentry.SanicSentry(app)

    @app.websocket('/test')
    async def simple(request, ws):
        raise Exception

    ws_conn = await websocket_client.ws_connect('/test')
    msg = await ws_conn.receive()
    assert msg.type.value in {257, 258}
    await ws_conn.close()

    await asyncio.sleep(0.01)
    assert len(sentry_calls) == 1


class EverythingConverter(PathConverter):
    regex = '.*?'


class Service:
    def __init__(self, *, host, port):
        self.host = host
        self.port = port
        self.app = flask.Flask('test')
        self.app.url_map.converters['everything'] = EverythingConverter

        self.srv = make_server(host=self.host, port=self.port, app=self.app)
        self.server_thread = threading.Thread(target=self.run, daemon=True)

    def run(self):
        self.srv.serve_forever()

    @property
    def url(self):
        return 'http://{host}:{port}'.format(
            host=self.host, port=self.port)

    def __repr__(self):
        return '{cls}(url={url})'.format(
            cls=self.__class__.__name__,
            url=self.url,
        )

    def start(self):
        self.server_thread.start()

    def stop(self):
        self.srv.shutdown()
        self.server_thread.join()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
