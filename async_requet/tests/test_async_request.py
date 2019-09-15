import asyncio
import functools
import time

from async_requet.bankofficer_request import BankofficerRequest
from async_requet.result_writer import write_to_excel

ITEM_INDEX_LIST = [1, 2]


def request_done_callback(object, loop, future):
    assert future.result is not None
    assert object.get_request_data is not None
    assert isinstance(object.get_request_data, list)
    assert len(object.get_request_data) > 0
    dataframes = object.create_dataframe()
    write_to_excel(dataframes, ['main'])
    loop.stop()


class TestBankofficerRequest:

    def test_request_to_bankofficer(self, mock_server):
        time.sleep(1)

        bankofficer_request = BankofficerRequest()
        loop = asyncio.get_event_loop()
        tasks = [
            loop.create_task(
                bankofficer_request.request_branches_transaction(index)
            )for index in ITEM_INDEX_LIST
        ]
        future = asyncio.ensure_future(asyncio.gather(*tasks))
        future.add_done_callback(
            functools.partial(request_done_callback, bankofficer_request, loop)
        )
        loop.run_forever()
