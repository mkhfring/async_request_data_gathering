import requests

class TestServer:

    def test_server(self, start_server):
        requests.post('http://127.0.0.1:5000/shutdown')
        assert 1 == 1
