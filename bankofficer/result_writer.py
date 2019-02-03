import os

import xlsxwriter
import pandas as pd

from bankofficer import MAIN_DIRECTORY
from bankofficer.bankofficer_request import BankofficerRequest
from balebot.utils.logger import Logger


logger = Logger.get_logger()


excel_path = '{}/data/vip_report.xlsx'.format(MAIN_DIRECTORY)
report_result_path = '{}/data/bank_officer_request.csv'.format(MAIN_DIRECTORY)
omure_shoab_path = '{}/data/branche-omur.txt'.format(MAIN_DIRECTORY)
START_OF_THE_ROW = 0
OMUR_SHOAB_INDEX = 10
BRANCH_CODE_INDEX = 4
BRANCH_NAME_INDEX = 5


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

