import time
import requests


class TestMockServer:

    def test_mockserver(self, mock_server):
        time.sleep(1)
        response = requests.get('http://localhost:5000/todo/api/v1.0/tasks/2')
        assert response.json()['id'] == 2

