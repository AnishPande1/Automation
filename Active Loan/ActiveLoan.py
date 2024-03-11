from robocorp.tasks import tasks
from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
import os
import zipfile
import time
from config import *

@tasks
class Loan:

    def __init__(self):
        self.browser = Selenium()
        self.excel = Files()

    def open_website_and_download_excel(self):
        self.browser.open_available_browser("https://botsdna.com/ActiveLoans/")
        download_link = self.browser.get_element_attribute("/html/body/center/font/a[2]", 'href')
        self.browser.click_element(download_link)

        wait_time = 60  # Maximum wait time in seconds
        file_path = EXCEL_FILE_PATH
        start_time = time.time()

        while not os.path.exists(file_path):
            time.sleep(1)

            # Check if the maximum wait time is reached
            if time.time() - start_time > wait_time:
                raise TimeoutError(f"Download took too long. Maximum wait time of {wait_time} seconds exceeded.")

    def extract_last_four_digits_from_excel(self, row):
        account_number = self.excel.read_cell("Sheet1", row, 1)
        last_four_digits = account_number[-4:]
        return last_four_digits

    def find_row_with_last_four_digits(self, last_four_digits):
        rows = self.browser.find_elements("xpath=/html/body/center/table/tbody/tr")

        for i, row in enumerate(rows, start=1):
            loan_code = row.find_element("td[2]").text
            if last_four_digits in loan_code:
                return i

        return None

    def download_and_extract_zip_file(self, row_with_last_four_digits):
        zip_link_xpath = f"/html/body/center/table/tbody/tr[{row_with_last_four_digits}]/td[2]/a"
        zip_link = self.browser.get_element_attribute(zip_link_xpath, 'href')

        # Extract last four digits from the link
        last_four_digits_start_index = zip_link.rfind('-') + 1
        last_four_digits = zip_link[last_four_digits_start_index:]

        self.browser.click_element(zip_link)

        time.sleep(10)  # Wait for the download to complete

        with zipfile.ZipFile(ZIP_FILE_PATH, 'r') as zip_ref:
            zip_ref.extractall("extracted_files")

    def read_and_fill_excel_from_text_file(self, row):
        text_file_path = TEXT_FILE_PATH
        with open(text_file_path, 'r') as text_file:
            # Read data from the text file (adjust the logic based on your file structure)
            data_from_text_file = {}  # Replace this with your logic

            # Fill the missing details in the Excel file
            self.excel.write_to_cells("Sheet1", row, 4, data_from_text_file.get("Loan Taken On", ""))
            self.excel.write_to_cells("Sheet1", row, 5, data_from_text_file.get("Amount", ""))
            self.excel.write_to_cells("Sheet1", row, 6, data_from_text_file.get("EMI(Monthly)", ""))

    def fill_missing_details_from_website(self, row_with_last_four_digits):
        status_xpath = f"/html/body/center/table/tbody/tr[{row_with_last_four_digits}]/td[1]"
        pan_number_xpath = f"/html/body/center/table/tbody/tr[{row_with_last_four_digits}]/td[3]"

        status = self.browser.get_text(status_xpath)
        pan_number = self.browser.get_text(pan_number_xpath)

        self.excel.write_to_cells("Sheet1", row_with_last_four_digits, 3, status)
        self.excel.write_to_cells("Sheet1", row_with_last_four_digits, 9, pan_number)

    def execute(self):
        try:
            # Open website and download Excel
            self.open_website_and_download_excel()

            # Get the total number of rows in the Excel file
            total_rows = self.excel.get_used_rows("Sheet1")

            # Iterate through each row in the Excel file
            for row in range(2, total_rows + 1):
                # Extract last four digits from the current row in the Excel file
                last_four_digits = self.extract_last_four_digits_from_excel(row)

                # Find the row with the corresponding last four digits in the loan code
                row_with_last_four_digits = self.find_row_with_last_four_digits(last_four_digits)

                if row_with_last_four_digits:
                    # Go back to the website and find the corresponding details
                    self.open_website_and_download_excel()

                    # Download and extract the zip file
                    self.download_and_extract_zip_file(row_with_last_four_digits)

                    # Read and fill Excel from the text file
                    self.read_and_fill_excel_from_text_file(row)

                    # Fill missing details from the website
                    self.fill_missing_details_from_website(row)

        finally:
            self.browser.close_browser()


# Uncomment the following lines if you want to run this as a standalone script
# if __name__ == "__main__":
#     loan_automation = LoanAutomation()
#     loan_automation.execute()
