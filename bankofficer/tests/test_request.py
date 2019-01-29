import os
import asyncio

import yaml

from bankofficer.login import login
from bankofficer.bankofficer_request import BankofficerRequest
from bankofficer.asyncrequest import get_shoab_list
from bankofficer import MAIN_DIRECTORY
from bankofficer.result_writer import write_to_excel
import functools


CONF_PATH = '{}/sensetive_conf.yml'.format(MAIN_DIRECTORY)
with open(CONF_PATH) as file:
    settings = yaml.load(file.read())
shoab_list = get_shoab_list()


def request_done_callback(object, loop, future):
    assert future.result is not None
    assert object.get_request_data is not None
    assert isinstance(object.get_request_data, list)
    assert len(object.get_request_data) > 0
    fields = [
        key for key, value in object.get_request_data[0] \
        .items()
    ]
    assert fields is not None
    response_body = object.get_data_body()
    assert len(response_body) > 0
    assert isinstance(response_body, list)
    write_to_excel(response_body, fields)
    assert os.path.exists('{}/data/vip_report.xlsx'.format(MAIN_DIRECTORY))
    loop.stop()


class TestBankofficerRequest:

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
        tasks.append(
            loop.create_task(
                bankofficer_request.request_branches_transaction()
            )
        )
        future = asyncio.ensure_future(asyncio.gather(*tasks))
        future.add_done_callback(
            functools.partial(request_done_callback, bankofficer_request, loop)
        )
        loop.run_forever()
