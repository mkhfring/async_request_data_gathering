from datetime import datetime, timedelta
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

    # def get_data_body(self):
    #     result = []
    #     for element in self.get_request_data:
    #         result.append([value for value in element.values()])
    #
    #     return result
    #
    def create_dataframe(self):
        main_dataframe = defaultdict(list)
        fields = [key for key in self.get_request_data[0].keys()]

        for element in self.get_request_data:
            for key, value in element.items():
                main_dataframe[key].append(value)


        return (main_dataframe,)
    #
    # @staticmethod
    # def get_omur_shoab(file_path):
    #
    #     def get_branch(data):
    #         return data[0]
    #
    #     def get_omure_shobe(data):
    #         return data[1]
    #
    #     result = {}
    #     with open(file_path, 'r') as file:
    #         for line in file:
    #             line = line.rstrip().split(',')
    #             result[get_branch(line)] = get_omure_shobe(line)
    #
    #     return result

    @property
    def get_request_data(self):
        return self.request_result
