from datetime import datetime, timedelta

import aiohttp

from bankofficer import MAIN_DIRECTORY


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
                print(response.status)
                result = await response.json()
                for element in result:
                    element['branchCode'] = shobe
                    self.request_result.append(element)

    def get_data_body(self):
        result = []
        for element in self.get_request_data:
            result.append([value for value in element.values()])

        return result

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
