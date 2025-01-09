from bs4 import BeautifulSoup
import time
from captcha_solver import solve_captcha

def scrape(sb, url):
    sb.uc_open_with_reconnect(url)
    solve_captcha(sb)
    
    sb.set_messenger_theme(location="top_left")
    sb.post_message("SeleniumBase wasn't detected", duration=3)

    page_source = sb.get_page_source()
    soup = BeautifulSoup(page_source, 'html.parser')

    # Extract elements with the class name 'novel-item'
    novel_items = soup.find_all(class_="novel-item")

    # Process the extracted items
    for index, item in enumerate(novel_items, start=1):
        print(f"Novel {index}:")

        # Extract title
        title_tag = item.find("a", title=True)
        title = title_tag["title"] if title_tag else "Unknown Title"

        # Extract link
        link = title_tag["href"] if title_tag else "No Link"
        link = f"https://www.lightnovelcave.com{link}" if link.startswith("/") else link

        # Extract image
        figure_tag = item.find("figure", class_="novel-cover")
        image_tag = figure_tag.find("img") if figure_tag else None
        image_url = image_tag["src"] if image_tag else "No Image"

        # Print details one by one with a pause
        print(f"Title: {title}")
        time.sleep(1)  # Pause between printing details

        print(f"Link: {link}")
        time.sleep(1)

        print(f"Image URL: {image_url}")
        time.sleep(1)

        print("-" * 80)
    
    print(f"Total novels found: {len(novel_items)}")
    print("Scraped")
    
    time.sleep(300)
