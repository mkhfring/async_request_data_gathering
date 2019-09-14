import sys
import asyncio
import functools
from datetime import datetime

import yaml
from balebot.utils.logger import Logger

from async_requet.login import login
from async_requet import MAIN_DIRECTORY
from async_requet.asyncrequest import get_shoab_list
from async_requet.result_writer import write_to_excel
from async_requet.bankofficer_request import BankofficerRequest
from async_requet.exeptions import RequestException


logger = Logger().get_logger()


CONF_PATH = '{}/sensetive_conf.yml'.format(MAIN_DIRECTORY)
with open(CONF_PATH) as file:
    settings = yaml.load(file.read())
shoab_list = get_shoab_list()


def request_done_callback(object, loop, future):

    dataframes = object.create_dataframe()
    write_to_excel(dataframes, ['branches', 'main'])


def create_report(loop):

    cookie = None
    try:
        cookie = login(
            settings['login']['username'],
            settings['login']['password'],
            settings['login']['url']
        )
    except RequestException as e:
        logger.error(e, extra={
            'step': sys._getframe().f_code.co_name,
            'time': datetime.now()
        })

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

    future = asyncio.ensure_future(asyncio.gather(*tasks))
    future.add_done_callback(
        functools.partial(request_done_callback, bankofficer_request, loop)
    )
