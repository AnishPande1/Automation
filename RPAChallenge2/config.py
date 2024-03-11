import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RESULTS_DIR = os.path.join(BASE_DIR, 'output')
LOGS_DIR = os.path.join(RESULTS_DIR, 'logs')
ERRORS_DIR = os.path.join(RESULTS_DIR, 'errors')
IMAGES_DIR = os.path.join(RESULTS_DIR, 'images')

LOG_FILE = 'basic.log'
EXCEPTION_SCREENSHOT = 'error_screenshot.png'
EXCEL_FILE = 'fresh_news.xlsx'

DATE_PATTERN = r'(\d{1,2} (minute|hour|day)s? ago|\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1,2}, \d{4}\b)'

for dir_path in [RESULTS_DIR, LOGS_DIR, ERRORS_DIR, IMAGES_DIR]:
    os.makedirs(dir_path, exist_ok=True)
