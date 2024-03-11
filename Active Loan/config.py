import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, 'output')

for dir_path in [RESULTS_DIR]:
    os.makedirs(dir_path, exist_ok=True)

EXCEL_FILE_PATH = os.path.join(RESULTS_DIR, 'input.xslx')
ZIP_FILE_PATH = os.path.join(RESULTS_DIR, 'loan_details.zip')
TEXT_FILE_PATH = os.path.join(RESULTS_DIR, 'account_details.txt')