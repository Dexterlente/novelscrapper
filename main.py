import os
import random
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Import your scraping logic.
from logic.scrapper import scrape

load_dotenv()

class LightNovelScraper:
    def __init__(self, url: str, proxy: str = None, use_proxy_probability: float = 0.5):
        self.url = url
        self.proxy = proxy
        self.use_proxy_probability = use_proxy_probability

    def start_session(self):
        # Randomly decide whether to use the provided proxy.
        selected_proxy = self.proxy if random.random() < self.use_proxy_probability else None

        chrome_options = Options()
        # Run Chrome in headless mode.
        chrome_options.add_argument("--headless=new")  # Updated headless mode flag
        # Set a window size to help mimic a real browser.
        chrome_options.add_argument("--window-size=1920,1080")
        # Disable GPU and sandboxing for stability in headless mode.
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        # Set a common user-agent to replicate a real browser.
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

        # Remove automation flags to avoid detection.
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        # Enable browser logs.
        chrome_options.set_capability("goog:loggingPrefs", {"browser": "INFO"})

        if selected_proxy:
            chrome_options.add_argument(f'--proxy-server={selected_proxy}')

        # Instantiate the Chrome WebDriver with the options.
        driver = webdriver.Chrome(service=Service(), options=chrome_options)
        driver.implicitly_wait(5)  # Reduced wait time
        return driver

# Retrieve your proxy setting from environment variables.
BRIGHTDATA_PROXY = os.getenv('BRIGHTDATA_PROXY')

# Define the URL to scrape.
url = "https://www.lightnovelcave.com/browse/genre-action-04061342/order-new/status-all?page=10"
scraper = LightNovelScraper(url, BRIGHTDATA_PROXY, use_proxy_probability=0.0)

# Start the Selenium session and run the scraper.
driver = scraper.start_session()
try:
    scrape(driver, scraper.url)
finally:
    driver.quit()
