import os
import csv

import xlsxwriter
import pandas as pd

from async_requet import MAIN_DIRECTORY
from async_requet.bankofficer_request import BankofficerRequest
from balebot.utils.logger import Logger


logger = Logger.get_logger()


excel_path = '{}/data/vip_report.xlsx'.format(MAIN_DIRECTORY)
report_result_path = '{}/data/bank_officer_request.csv'.format(MAIN_DIRECTORY)
omure_shoab_path = '{}/data/branche-omur.txt'.format(MAIN_DIRECTORY)
START_OF_THE_ROW = 0
OMUR_SHOAB_INDEX = 10
BRANCH_CODE_INDEX = 4
BRANCH_NAME_INDEX = 5


class ResultWriter:

    def __init__(self, data):
        self.data = data

    def write_to_csv(self, filename, fieldnames):
        if os.path.exists(filename):
            os.remove(filename)

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for element in self.data:
                writer.writerow(element)

    def write_to_excel(self, filename):
        self.headers = self.get_headers
        workbook = xlsxwriter.Workbook(filename)
        field_values = list(self.get_field_values('کد شعبه'))
        for value in field_values:
            self.write_to_worksheet(workbook, value)

        workbook.close()

    @property
    def get_headers(self):
        return [key for key in self.data[0].keys()]

    def get_data_body(self, data):
        result = []
        for element in data:
            result.append([value for value in element.values()])

        return result

    def get_field_values(self, field):
        result = []
        for element in self.data:
            result.append(element[field])

        return set(result)

    def filter_by_field_value(self, value):
        result = []
        for element in self.data:
            if value in element.values():
                result.append(element)

        return result

    def write_to_worksheet(self, workbook, case):
        case_worksheet = workbook.add_worksheet('{}'.format(case))
        bold = workbook.add_format({'bold': True})
        case_worksheet.write_row('A1', self.headers, bold)
        shoab_case = self.filter_by_field_value(case)
        shoab_data_body = self.get_data_body(shoab_case)
        for row, element in enumerate(shoab_data_body):
            case_worksheet.write_row(row+1, 0, element)


def branch_code(data):
    return data[4]


def write_to_excel(dataframe_tuple, sheet_name_list):
    if os.path.exists(excel_path):
        os.remove(excel_path)

    writer = pd.ExcelWriter(excel_path)
    branch_df = pd.DataFrame(dataframe_tuple[0])
    branch_df.sort_values(by=['branchCode'], ascending=True)
    main_df = pd.DataFrame(dataframe_tuple[1])
    branch_df.to_excel(writer, sheet_name_list[0])
    main_df.to_excel(writer, sheet_name_list[1])
    writer.save()

