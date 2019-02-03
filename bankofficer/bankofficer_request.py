from datetime import datetime, timedelta
from collections import defaultdict

import aiohttp
from balebot.utils.logger import Logger

from bankofficer.exeptions import RequestException


logger = Logger().get_logger()


class BankofficerRequest:
    def __init__(self, cookie):
        self.cookie = cookie
        self.headers = {
        'Cookie': self.cookie,
        'Content-Type': 'application/json'
         }
        self.request_result = []

    async def request_branches_transaction(self, shobe=''):

        base_time = datetime.today() - timedelta(2)
        start_date = int(base_time.replace(
            hour=0,
            minute=0,
            second=0
        ).timestamp()) * 1000
        end_date = int(base_time.replace(
            hour=23,
            minute=59,
            second=59
        ).timestamp()) * 1000

        request_headers = {
            'Cookie': self.cookie,
            'Content-Type': 'application/json'
        }
        request_url = 'https://admportal.bmi.ir/portalserver/services/rest/' \
                      'accountOfficer/statistics/' \
                      'allRequestsWithScores/{}/{}?' \
                      'branchCode={}&pageSize=100&pageNo=0'.format(
            start_date,
            end_date,
            shobe
        )

        async with aiohttp.ClientSession() as session:
            async with session.get(
                    request_url, headers=request_headers
            ) as response:
                if response.status != 200:
                    raise RequestException(
                        'Bankofficer request fail, status: {}' \
                            .format(response.status)
                    )
                logger.info(
                    'Status code: {}, time:{}' \
                        .format(response.status, datetime.now())
                )
                result = await response.json()
                for element in result:
                    element['branchCode'] = shobe
                    self.request_result.append(element)

    def get_data_body(self):
        result = []
        for element in self.get_request_data:
            result.append([value for value in element.values()])

        return result

    def create_dataframe(self):
        branches_dataframe = defaultdict(list)
        main_dataframe = defaultdict(list)
        fields = [key for key in self.get_request_data[0].keys()]

        for element in self.get_request_data:
            for key, value in element.items():
                if element['branchCode']:
                    branches_dataframe[key].append(value)
                else:
                    main_dataframe[key].append(value)

        del branches_dataframe['branchName']
        del main_dataframe['branchName']
        del main_dataframe['branchCode']

        return branches_dataframe, main_dataframe

    @staticmethod
    def get_omur_shoab(file_path):

        def get_branch(data):
            return data[0]

        def get_omure_shobe(data):
            return data[1]

        result = {}
        with open(file_path, 'r') as file:
            for line in file:
                line = line.rstrip().split(',')
                result[get_branch(line)] = get_omure_shobe(line)

        return result

    @property
    def get_request_data(self):
        return self.request_result
