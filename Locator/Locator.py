from robocorp.tasks import tasks
from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
from config import *

@tasks
class locator:
    def __init__(self) -> None:
        self.browser = Selenium()
        self.files = Files()

    def open_url(self):
        self.browser.open_available_browser("https://botsdna.com/locator/")

    def sort_data(self):
        table_locator = "/html/body/center/table[4]/tbody"
        self.browser.wait_until_element_is_visible(table_locator)

        header_row = self.browser.find_element(f"{table_locator}/tr[1]")
        country_names = [col.text for col in header_row.find_elements("td")[1:]]  # Exclude the first column with customer names

        for country_name in country_names:
            country_data = self.get_customer_data_for_country(table_locator, country_name)
            if country_data:
                self.write_sheet_to_excel(country_name, country_data)

    def get_customer_data_for_country(self, table_locator, country_name):
        customer_data = []

        # Assuming each row represents a customer and each column is a country
        rows = self.browser.find_elements(f"{table_locator}/tr")
        header_row = rows[0]
        country_index = header_row.find_elements("td").index(header_row.find_element(f"td[contains(text(), '{country_name}')]"))

        for row in rows[1:]:
            customer_name = row.find_element("td[1]").text
            amount = int(row.find_elements("td")[country_index].text)

            # Skip customers with zero amount for the current country
            if amount != 0:
                customer_data.append({"Name": customer_name, "Amount": amount})

        return customer_data

    def write_sheet_to_excel(self, country_name, customer_data):
        sheet_name = country_name

        # If the sheet already exists, remove it
        if self.files.sheet_exists(EXCEL_FILE_PATH):
            self.files.remove_sheet(EXCEL_FILE_PATH)

        # Add a new sheet for the current country
        self.files.add_sheet(EXCEL_FILE_PATH, sheet_name)

        # Write headers
        headers = ["Customer Name", "Amount"]
        start_row, start_column = 1, 1
        self.files.write_to_cells(EXCEL_FILE_PATH, sheet_name, start_row, start_column, [headers])

        # Write customer data
        start_row += 1
        self.files.write_to_cells(EXCEL_FILE_PATH, sheet_name, start_row, start_column, customer_data)

    def close_url(self):
        self.browser.close_browser()
