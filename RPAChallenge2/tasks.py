
from News import AljazeeraNews
from workitems import fetch_workitems
from config import *


def task() -> None:
    try:
        work_items = fetch_workitems()
        fresh_news = AljazeeraNews(work_items)
        fresh_news.open_website()
        fresh_news.perform_search()
        fresh_news.start_date()
        fresh_news.sort_by_date()
        fresh_news.excel_file()
        fresh_news.click_show_more_button()
        search_phrases = fresh_news.search_term.lower().split()
        fresh_news.scrape_news_data(search_phrases)
    except Exception as e:
        print(f"An error occurred: {e}")
        screenshot_path = os.path.join(ERRORS_DIR, EXCEPTION_SCREENSHOT)
        fresh_news.take_screenshot(screenshot_path)


if __name__ == '__main__':
    task()
