from seleniumbase import SB
from logic.scrapper import scrape

class LightNovelScraper:
    def __init__(self, url: str):
        self.url = url
    
    def start_session(self):
        return SB(uc=True, headless=False, test=True)


url = "https://www.lightnovelcave.com/browse/genre-action-04061342/order-new/status-all"
scraper = LightNovelScraper(url)

with scraper.start_session() as sb:
    scrape(sb, scraper.url)
