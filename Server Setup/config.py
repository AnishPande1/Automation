import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, 'output')

for dir_path in [RESULTS_DIR]:
    os.makedirs(dir_path, exist_ok=True)

EXCEL_FILE_PATH = os.path.join(RESULTS_DIR, 'input.xlsx')
# SMTP server configuration
SMTP_SERVER = 'your_smtp_server.com'
SMTP_PORT = 587
SMTP_USERNAME = 'your_smtp_username'
SMTP_PASSWORD = 'your_smtp_password'
EMAIL_FROM = 'your_email@example.com'
EMAIL_USERNAME='your_email.id'
EMAIL_PASSWORD='your_password'
#make changes as per your configuration