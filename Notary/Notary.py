from robocorp import tasks
from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
import time
from config import *

@tasks
class Notaries:
    def __init__(self):
        self.browser = Selenium()
        self.excel = Files()

    def open_website_and_download_excel(self):
        self.browser.open_available_browser("https://example.com")  # Replace with your website URL

        self.browser.click_element("/html/body/center/font/a[2]")

        wait_time = 60  # Maximum wait time in seconds
        file_path = EXCEL_FILE_PATH
        start_time = time.time()

        while not os.path.exists(file_path):
            time.sleep(1)

            # Check if the maximum wait time is reached
            if time.time() - start_time > wait_time:
                raise TimeoutError(f"Download took too long. Maximum wait time of {wait_time} seconds exceeded.")

    def fill_form_and_submit(self, district_name, practitioner_name, area_of_practice):
        # Assuming there is a dropdown to select the district on the website
        self.browser.wait_until_element_is_visible("/html/body/center/table[2]/tbody/tr[4]/td[2]")
        self.browser.select_frame("/html/body/center/table[2]/tbody/tr[3]/td[2]/select", district_name)

        # Fill the form with data
        self.browser.input_text("/html/body/center/table[2]/tbody/tr[1]/td[2]", practitioner_name)
        self.browser.input_text("/html/body/center/table[2]/tbody/tr[2]/td[2]", area_of_practice)

        # Click the submit button
        self.browser.click_button("/html/body/center/table[2]/tbody/tr[4]/td[2]")

        # Get and save the transaction number from the page
        self.browser.wait_until_element_is_visible("/html/body/center/h1/p")
        transaction_number = self.browser.get_text("/html/body/center/h1/p")
        self.browser.go_back()
        return transaction_number

    def execute(self):
        try:
            # Open website and download Excel
            self.open_website_and_download_excel()

            # Open and read the Excel file
            self.excel.open_workbook(EXCEL_FILE_PATH)
            
            # Iterate through each row in the Excel file
            for row in range(2, self.excel.get_used_rows("Sheet1") + 1):
                # Extract data from the Excel file
                district_name = self.excel.read_cell("Sheet1", row, 1)
                practitioner_name = self.excel.read_cell("Sheet1", row, 2)
                area_of_practice = self.excel.read_cell("Sheet1", row, 3)

                # Fill the form and get the transaction number
                transaction_number = self.fill_form_and_submit(district_name, practitioner_name, area_of_practice)

                # Update the Excel file with the transaction number
                self.excel.write_to_cells("Sheet1", row, 4, transaction_number)

        finally:
            # Save and close the Excel file
            self.excel.save_workbook(EXCEL_FILE_PATH)
            self.excel.close_workbook()

            # Close the browser
            self.browser.close_browser()


# Uncomment the following lines if you want to run this as a standalone script
# if __name__ == "__main__":
#     form_fill_automation = FormFillAutomation()
#     form_fill_automation.execute()
