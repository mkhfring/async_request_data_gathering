import asyncio
import functools

import yaml

from bankofficer.login import login
from bankofficer import MAIN_DIRECTORY
from bankofficer.asyncrequest import get_shoab_list
from bankofficer.result_writer import write_to_excel
from bankofficer.bankofficer_request import BankofficerRequest


CONF_PATH = '{}/sensetive_conf.yml'.format(MAIN_DIRECTORY)
with open(CONF_PATH) as file:
    settings = yaml.load(file.read())
shoab_list = get_shoab_list()


def request_done_callback(object, loop, future):
    fields = [
        key for key, value in object.get_request_data[0] \
            .items()
    ]
    response_body = object.get_data_body()

    # TODO: Log if the response was empty
    write_to_excel(response_body, fields)


def create_report(loop):

    # TODO: Log the state of the login
    cookie = login(
        settings['login']['username'],
        settings['login']['password'],
        settings['login']['url']
    )
    bankofficer_request = BankofficerRequest(cookie)
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

    # TODO: Log the state of the request
    future = asyncio.ensure_future(asyncio.gather(*tasks))
    future.add_done_callback(
        functools.partial(request_done_callback, bankofficer_request, loop)
    )
