from RPA.Browser.Selenium import Selenium
import pandas as pd
from config import *

class SPFTool:
    def __init__(self):
        self.browser=Selenium() 

    def open_browser(self):
        self.browser.open_available_browser("https://www.kitterman.com/spf/validate.html?")
    
    def read_excel_and_fill_form(self):
        df=pd.read_excel(EXCEL_FILE_PATH)
        for domain in df["Domain names"]:
            self.browser.input_text("//tr/td[text()='Domain name: ']/following-sibling::td/input[@name='domain']", domain)
            self.browser.click_element("//input[@value='Get SPF Record (if any)' and @type='submit']")
            self.browser.capture_page_screenshot(f"{domain}_validation result.png")
            self.browser.click_element("//input[@value='Return to SPF checking tool (clears form)']")
    
    def close(self):
        self.browser.close_browser()

