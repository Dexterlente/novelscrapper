from seleniumbase import SB
from bs4 import BeautifulSoup
import time
from captcha_solver import solve_captcha

class LightNovelScraper:
    def __init__(self, url: str):
        self.url = url
    
    def start_session(self):
        return SB(uc=True, headless=False, test=True)
    
    def scrape(self, sb):
        sb.uc_open_with_reconnect(self.url)
        solve_captcha(sb)
        
        sb.set_messenger_theme(location="top_left")
        sb.post_message("SeleniumBase wasn't detected", duration=3)

        page_source = sb.get_page_source()
        soup = BeautifulSoup(page_source, 'html.parser')

        body_content = soup.body.prettify()
        print(body_content)
        
        print("Scraped")
 
        time.sleep(300)

url = "https://www.lightnovelcave.com/browse/genre-action-04061342/order-new/status-all"
scraper = LightNovelScraper(url)

# Start the session
with scraper.start_session() as sb:
    # Perform the scraping logic
    scraper.scrape(sb)
