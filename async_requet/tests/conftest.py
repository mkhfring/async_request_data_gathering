import pytest

from async_requet.tests.helpers import MockServer


@pytest.fixture
def mock_server(request):
    server = MockServer()
    server.start()
    yield server
    server.shutdown_server()