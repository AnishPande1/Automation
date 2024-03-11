
from RPA.Browser.Selenium import Selenium   
#from RPA.Desktop import Desktop
from selenium.common.exceptions import NoSuchElementException
from SeleniumLibrary.errors import ElementNotFound
from datetime import datetime, timedelta
from retry import retry
from loggers import setup_logger
from config import *
import pandas as pd
import zipfile
import requests
import re
from typing import List


class AljazeeraNews:
    def __init__(self, work_item) -> None:
        self.browser = Selenium()
        #self.desktop=Desktop()
        self.search_term = work_item["search_term"]
        self.number_of_months = work_item["number_of_months"]
        self.logger = setup_logger(LOGS_DIR)

    def open_website(self) -> None:
        self.logger.info("Opening the Al Jazeera website.")
        self.browser.open_available_browser("https://www.aljazeera.com/", maximized=True)
        self.browser.wait_until_element_is_visible("//div[@class='site-header__search-trigger']//button")
        self.browser.click_element("//div[@class='site-header__search-trigger']//button")
        self.logger.info("Website opened successfully.")

    def perform_search(self) -> None:
        self.logger.info(f"Performing a search for '{self.search_term}'.")
        self.browser.wait_until_element_is_visible("//*[@id='root']/div/div[1]/div/div/div[1]/div/header/nav/ul/li[1]/form/div[1]/input")
        self.browser.input_text("//*[@id='root']/div/div[1]/div/div/div[1]/div/header/nav/ul/li[1]/form/div[1]/input", self.search_term)
        self.browser.click_element("//*[@id='root']/div/div[1]/div/div/div[1]/div/header/nav/ul/li[1]/form/div[1]/div")
        self.logger.info("Search operation completed successfully.")

    def sort_by_date(self) -> None:
        self.logger.info("Applying sorting by date.")
        self.browser.wait_until_element_is_visible("//span[@class='search-summary__query']")
        self.browser.wait_until_element_is_visible("//*[@id='main-content-area']/div[2]/div[2]")
        self.browser.select_from_list_by_value("//*[@id='search-sort-option']", "Date")
        self.logger.info("Sorting by date applied successfully.")

    @retry((ElementNotFound), 5, 5)
    def show_more_button_actions(self) -> None:
        show_more_button = self.browser.find_element("//button[@class='show-more-button grid-full-width']/span[2]")
        self.logger.info("Clicking the 'Show more' button.")
        self.browser.driver.execute_script(
            "arguments[0].scrollIntoView({ behavior: 'auto', block: 'center', inline: 'center' }); window.scrollBy(0, -100);",
            show_more_button
        )
        self.browser.click_element("//button[@class='show-more-button grid-full-width']/span[2]")
        self.logger.info("Clicked 'Show more' button successfully.")

    def click_show_more_button(self) -> None:
        self.logger.info("Clicking the 'Show more' button repeatedly.")
        try:
            while True:
                self.show_more_button_actions()
        except NoSuchElementException:
            self.logger.info("No more additional news articles found.")
        except Exception as e:
            self.logger.info(f"An error occurred while clicking 'Show more' button: {str(e)}")

    def start_date(self):
        if self.number_of_months < 0:
            raise ValueError("Number of months cannot be negative.")
        self.logger.info(f"Calculating target start date for {self.number_of_months} months.")

        current_date = datetime.now()
        start_date = current_date.replace(day=1)

        if self.number_of_months > 1:
            start_date -= timedelta(days=start_date.day)
            for _ in range(self.number_of_months - 1):
                start_date -= timedelta(days=start_date.day)

        self.logger.info(f"Target start date: {start_date}")
        return start_date
    
    def excel_file(self) -> None:
        excel_file_path = os.path.join(RESULTS_DIR, EXCEL_FILE)
        self.df = pd.DataFrame(columns=['Title', 'Description', 'Date', 'Image Path', 'Search Term Count', 'Money Present'])
        self.excel_file_path = excel_file_path
        self.df.to_excel(self.excel_file_path, index=False)
    
    def extract_and_format_dates(self, text):
        date_matches = re.findall(DATE_PATTERN, text)
        extracted_dates = []

        for match in date_matches:
            if 'minute' in match[0] or 'hour' in match[0] or 'day' in match[0]:
                time_unit = match[0].split()[1]
                time_amount = int(match[0].split()[0])
                if 'minute' in time_unit:
                    date = datetime.now() - timedelta(minutes=time_amount)
                elif 'hour' in time_unit:
                    date = datetime.now() - timedelta(hours=time_amount)
                elif 'day' in time_unit:
                    date = datetime.now() - timedelta(days=time_amount)
                extracted_dates.append(date.strftime('%d/%m/%Y'))
            else:
                try:
                    date = datetime.strptime(match[0], '%b %d, %Y')
                    extracted_dates.append(date.strftime('%d/%m/%Y'))
                except ValueError:
                    self.logger.info(f"Failed to parse date: {match[0]}")

        formatted_dates = ", ".join(extracted_dates) 
        return formatted_dates

    def download_images(self, image_urls) -> List[str]:
        image_paths = []
        for i, image_url in enumerate(image_urls, start=1):
            if image_url:
                image_filename = os.path.join(IMAGES_DIR, f"image_{i}.jpg")
                try:
                    response = requests.get(image_url)
                    response.raise_for_status()
                    with open(image_filename, "wb") as img_file:
                        img_file.write(response.content)
                    self.logger.info(f"Image {i} downloaded successfully.")
                    image_paths.append(image_filename)
                except requests.exceptions.RequestException as e:
                    self.logger.info(f"Error downloading image {i}: {str(e)}")
                except Exception as e:
                    self.logger.info(f"Error downloading image {i}: {str(e)}")

        zip_filename = os.path.join(RESULTS_DIR, "downloaded_images.zip")
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for image_path in image_paths:
                zipf.write(image_path, os.path.basename(image_path))
        
        self.logger.info(f"Downloaded images have been zipped to {zip_filename}")
        return image_paths

    def count_search_phrase_occurrences(self, search_phrase, titles, descriptions):
        counts = [title.lower().count(search_phrase) + desc.lower().count(search_phrase) for title, desc in zip(titles, descriptions)]
        self.logger.info(f"Counted occurrences of '{search_phrase}' in titles and descriptions.")
        return counts
    
    def check_for_money(self, text):
        money_pattern = r'\$[\d,]+(\.\d{1,2})?|\d+ dollars|\d+ USD'

        if re.search(money_pattern, text):
            return True
        else:
            return False

    def scrape_news_data(self, search_phrases):
        titles, descriptions, image_paths, money_present_values, article_dates = [], [], [], [], []
        article_box_locator = "//article[@class='gc u-clickable-card gc--type-customsearch#result gc--list gc--with-image']"
        article_boxes = self.browser.find_elements(article_box_locator) # type: ignore
        start_date = self.start_date()

        for i, element in enumerate(article_boxes, start=1):
            news_title, news_description, image_url = '', '', ''

            try:
                news_title = self.browser.get_text(f'//*[@id="main-content-area"]/header/h1')
                news_title = news_title.replace("­", "").replace("'", "")
            except ElementNotFound:
                pass

            try:
                news_description = self.browser.get_text(f'(//*[@id="main-content-area"]/div[3])[{i}]')
                news_description = news_description.replace("­", "").replace("'", "")
            except ElementNotFound:
                pass

            try:
                image_url = self.browser.get_element_attribute(f'(//*[@id="main-content-area"]/figure/div/img)[{i}]', 'src')
            except ElementNotFound:
                pass
            
            article_date = self.extract_and_format_dates(news_description)
            article_datetime = datetime.strptime(article_date, '%d/%m/%Y')
            
            if (article_datetime >= start_date):
                titles.append(news_title)
                descriptions.append(news_description)
                image_paths.append(image_url)
                article_dates.append(article_date)

        scraped_data = {
            'Title': titles,
            'Description': descriptions,
            'Date': article_dates,
            'Image Path': image_paths,
        }

        downloaded_image_paths = self.download_images(image_paths)
        scraped_data['Image Path'] = downloaded_image_paths
        
        for phrase in search_phrases:
            count_attribute = self.count_search_phrase_occurrences(phrase, titles, descriptions)
            scraped_data[f'Search Term Count'] = count_attribute

        for i in range(len(scraped_data['Title'])):
            money_present = self.check_for_money(scraped_data['Title'][i]) or self.check_for_money(scraped_data['Description'][i])
            money_present_values.append(money_present)

        scraped_data['Money Present'] = money_present_values
        
        scraped_df = pd.DataFrame(scraped_data)

        with pd.ExcelWriter(self.excel_file_path, engine='openpyxl', mode='a') as writer:
            try:
                writer.book.remove(writer.sheets['Sheet1'])
            except KeyError:
                pass

            scraped_df.to_excel(writer, sheet_name='Sheet1', index=False)

        self.logger.info(f"Scraped data saved to {self.excel_file_path}")
    
    def take_screenshot(self, filename) -> None:
        self.logger.info(f"Taking a screenshot and saving it as '{filename}'.")
        self.browser.capture_page_screenshot(filename)
        self.logger.info("Screenshot taken and saved successfully.")

