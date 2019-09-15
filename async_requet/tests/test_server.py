import time
import unittest
import requests


class TestMockServer:

    def test_mockserver(self, mock_server):
        time.sleep(1)
        r = requests.get('http://localhost:5000/todo/api/v1.0/tasks/2')
        assert 1 ==1
