import asyncio
import functools
import time

from async_requet.async_request_handler import AsyncRequestManager
from async_requet.result_writer import write_to_excel

ITEM_INDEX_LIST = [1, 2]


def request_done_callback(result_object, loop, future):
    assert future.result is not None
    assert result_object.get_request_data is not None
    assert isinstance(result_object.get_request_data, list)
    assert len(result_object.get_request_data) > 0
    dataframes = result_object.create_dataframe()
    write_to_excel(dataframes, ['main'])
    loop.stop()


class TestAsyncRequest:

    def test_async_request_and_write_to_db(self, mock_server):
        time.sleep(1)
        async_request_manager = AsyncRequestManager()
        loop = asyncio.get_event_loop()
        tasks = [
            loop.create_task(
                async_request_manager.request_to_server(index)
            )for index in ITEM_INDEX_LIST
        ]
        future = asyncio.ensure_future(asyncio.gather(*tasks))
        future.add_done_callback(
            functools.partial(request_done_callback, async_request_manager, loop)
        )
        loop.run_forever()
