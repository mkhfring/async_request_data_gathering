import os

import xlsxwriter

from bankofficer import MAIN_DIRECTORY
from bankofficer.bankofficer_request import BankofficerRequest


excel_path = '{}/data/vip_report.xlsx'.format(MAIN_DIRECTORY)
report_result_path = '{}/data/bank_officer_request.csv'.format(MAIN_DIRECTORY)
omure_shoab_path = '{}/data/branche-omur.txt'.format(MAIN_DIRECTORY)
START_OF_THE_ROW = 0
OMUR_SHOAB_INDEX = 10


def branch_code(data):
    return data[4]


def write_to_excel(data, fields):
    if os.path.exists(excel_path):
        os.remove(excel_path)

    omure_shoab_map = BankofficerRequest.get_omur_shoab(omure_shoab_path)
    workbook = xlsxwriter.Workbook(
        '{}/data/vip_report.xlsx'.format(MAIN_DIRECTORY)
    )
    main_sheet = workbook.add_worksheet('main')
    branch_sheet = workbook.add_worksheet('branches')
    main_sheet.write_row('A1', fields)
    branch_sheet.write_row('A1', fields)
    branch_sheet.write('K1', 'Omur Shoab')
    branches = [element for element in data if branch_code(element)]
    main = [element for element in data if not branch_code(element)]
    for index, element in enumerate(branches):
        branch_sheet.write_row(index+1, START_OF_THE_ROW, element)
        branch_sheet.write(
            index + 1,
            OMUR_SHOAB_INDEX,
            omure_shoab_map[str(int(branch_code(element)))]
        )

    for index, element in enumerate(main):
        main_sheet.write_row(index+1, START_OF_THE_ROW, element)

    workbook.close()
