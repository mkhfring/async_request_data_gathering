import os
import time
import asyncio
import calendar
from datetime import datetime, timedelta


import xlsxwriter
import aiohttp
import yaml

from async_requet.login import login


HERE = os.path.dirname(os.path.realpath(__file__))
CONF_PATH = os.path.join(HERE, 'sensetive_conf.yml')
with open(CONF_PATH) as file:
    settings = yaml.load(file.read())

# headers = login()
Setcookie = 'aa92fd0d02c4af6ed831aa2b09607ee2;'
excel_path = os.path.join(HERE, 'data/vip_report.xlsx')
report_result_path = os.path.join(HERE, 'data/bank_officer_request.csv')
account_officer_shoab = os.path.join(HERE, 'data/shoab.txt')


if os.path.exists(excel_path):
    os.remove(excel_path)

omur_shoab_dic = {}
requests_final_result = []


def get_shoab_list(file_path=account_officer_shoab):
    with open(file_path, 'r') as f:
        for line in f:
            shoab_list = line.rstrip().split(' ')

    return shoab_list


def get_data_body(data):
    result = []
    for element in data:
        result.append([value for value in element.values()])

    return result


def get_omur_shoab(file_path=os.path.join(HERE, 'data/branche-omur.txt')):
    result = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.rstrip().split(',')
            result[line[0]] = line[1]

    return result


def get_data_body(data):
    result = []
    for element in data:
        result.append([value for value in element.values()])

    return result


def write_to_excel(data, fileds):
    workbook = xlsxwriter.Workbook('./data/vip_report.xlsx')
    main_sheet = workbook.add_worksheet('main')
    branch_sheet = workbook.add_worksheet('branches')
    main_sheet.write_row('A1', fields)
    branch_sheet.write_row('A1', fields)
    branch_sheet.write('K1', 'Omur Shoab')
    branches = [element for element in data if element[4]]
    main = [element for element in data if not element[4]]
    for index, element in enumerate(branches):
        branch_sheet.write_row(index+1, 0, element)
        branch_sheet.write(index + 1, 10, omure_shoab_map[str(int(element[4]))])

    for index, element in enumerate(main):
        main_sheet.write_row(index+1, 0, element)

    workbook.close()


shoab_list = get_shoab_list()
omure_shoab_map = get_omur_shoab()


async def create_request(shobe=''):
    start_date = datetime.today() - timedelta(1)
    start_date = int(start_date.timestamp()) * 1000
    end_date = datetime.today() - timedelta(2)
    end_date = int(end_date.timestamp()) * 1000


    request_headers = {
        'Cookie': headers,
        'Content-Type': 'application/json'
    }
    request_url = 'https://admportal.bmi.ir/portalserver/services/rest/' \
                  'accountOfficer/statistics/' \
                  'allRequestsWithScores/1548028800000/1548072940120?' \
                  'branchCode={}&pageSize=100&pageNo=0'.format(shobe)

    async with aiohttp.ClientSession() as session:
        async with session.get(
                request_url, headers=request_headers
        ) as response:
            print(response.status)
            result = await response.json()
            for element in result:
                element['branchCode'] = shobe
                requests_final_result.append(element)


# loop = asyncio.get_event_loop()
# tasks = [asyncio.ensure_future(create_request(shobe)) for shobe in shoab_list]
# tasks.append(asyncio.ensure_future(create_request()))
#
# loop.run_until_complete(asyncio.wait(tasks))
# loop.close()
# fields = [key for key, value in requests_final_result[0].items()]
# response_body = get_data_body(requests_final_result)
# write_to_excel(response_body, fields)
