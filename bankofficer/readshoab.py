import os
import pandas as pd
import numpy as np


result = []
names = []
file_path = './data/shoab3.xlsx'
code_shoab_path = './data/code_shoab.xlsx'
result_path = './data/shoab.txt'
result_path2 = './data/shoab2-names.txt'
branch_omur = './data/branche-omur.txt'


if os.path.exists(result_path):
    os.remove(result_path)


if os.path.exists(result_path2):
    os.remove(result_path2)

exceldata = pd.ExcelFile(file_path)
print(exceldata.sheet_names)
data = exceldata.parse('Sheet1')
for index, row in data.iterrows():
        result.append(str(int(row['branchId'])))
        names.append(str(row['branchName']))

with open(result_path, 'w') as file:
    for element in result:
        file.write(element.zfill(4) + ' ')


branch_excel_data = pd.ExcelFile(code_shoab_path)
branch_omur_data = branch_excel_data.parse('Sheet1')

with open(branch_omur, 'w') as file:
    for index, row in branch_omur_data.iterrows():
        if not np.isnan(row['EdareOmorCode']):
            converted_row = int(row['EdareOmorCode'])
        else:
            converted_row = row['EdareOmorCode']

        file.write(str(int(row['UnitId'])) + ',' + str(converted_row) + '\n')


