import os
import random
from seleniumbase import SB
from logic.scrapper import scrape
from dotenv import load_dotenv

load_dotenv()

class LightNovelScraper:
    def __init__(self, url: str, proxy: str = None, use_proxy_probability: float = 0.5):
        self.url = url
        self.proxy = proxy
        self.use_proxy_probability = use_proxy_probability 
    

    def start_session(self):
        selected_proxy = self.proxy if random.random() < self.use_proxy_probability else None
        return SB(uc=True, headless=False, test=True,  proxy=selected_proxy)

BRIGHTDATA_PROXY = os.getenv('BRIGHTDATA_PROXY')


url = "https://www.lightnovelcave.com/browse/genre-action-04061342/order-new/status-all?page=53"
scraper = LightNovelScraper(url,BRIGHTDATA_PROXY, use_proxy_probability=0.4)

with scraper.start_session() as sb:
    scrape(sb, scraper.url)
  