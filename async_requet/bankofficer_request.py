from collections import defaultdict

import aiohttp

from async_requet.exeptions import RequestException


class BankofficerRequest:
    def __init__(self):
        self.request_result = []

    async def request_branches_transaction(self, item):

        request_url = 'http://localhost:5000/todo/api/v1.0/tasks/{}'.format(item)

        async with aiohttp.ClientSession() as session:
            async with session.get(request_url) as response:
                if response.status != 200:
                    raise RequestException(
                        'Bankofficer request fail, status: {}' \
                            .format(response.status)
                    )

                result = await response.json()
                self.request_result.append(result)

    def create_dataframe(self):
        main_dataframe = defaultdict(list)
        fields = [key for key in self.get_request_data[0].keys()]

        for element in self.get_request_data:
            for key, value in element.items():
                main_dataframe[key].append(value)

        return (main_dataframe,)

    @property
    def get_request_data(self):
        return self.request_result
