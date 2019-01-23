import os
import unittest
import asyncio

import yaml

from bankofficer.login import login
from bankofficer.bankofficer_request import BankofficerRequest
from bankofficer.asyncrequest import get_shoab_list


HERE = os.path.dirname(os.path.realpath(__file__))
CONF_PATH = os.path.join(HERE, '../sensetive_conf.yml')
with open(CONF_PATH) as file:
    settings = yaml.load(file.read())
shoab_list = get_shoab_list()


class TestBankofficerRequest(unittest.TestCase):

    def test_request_to_bankofficer(self):
        cookie = login(
            settings['login']['username'],
            settings['login']['password'],
            settings['login']['url']
        )
        assert cookie is not None
        assert 'Set-Cookie' in cookie
        bankofficer_request = BankofficerRequest(cookie)
        assert isinstance(bankofficer_request, BankofficerRequest)
        loop = asyncio.get_event_loop()
        tasks = [
            loop.create_task(
                bankofficer_request.request_branches_transaction(shobe)
            )for shobe in shoab_list
        ]
        loop.run_until_complete(asyncio.wait(tasks))

        assert bankofficer_request.get_requset_data is not None
        assert bankofficer_request.get_requset_data is not None
        assert len(bankofficer_request.get_requset_data) > 0
