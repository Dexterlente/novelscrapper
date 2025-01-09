from bs4 import BeautifulSoup
import time
from captcha_solver import solve_captcha

def scrape(sb, url):
    sb.uc_open_with_reconnect(url)
    solve_captcha(sb)
    
    sb.set_messenger_theme(location="top_left")
    sb.post_message("SeleniumBase wasn't detected", duration=3)

    while True:
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

        next_page_link = soup.find("li", class_="PagedList-skipToNext")
        if next_page_link:
            for retry_count in range(3):
                try:
                    next_page_url = next_page_link.find("a")["href"]
                    print(f"Going to next page: {next_page_url}")
                    sb.uc_open_with_reconnect(next_page_url)
                    time.sleep(3)
                    break
                except Exception as e:
                    print(f"Error occurred: {e}. Retrying...")
                    solve_captcha(sb)
                    time.sleep(2)
            else:
                print("No more retries, exiting scraping.")
                break
        else:
                print("No more pages to scrape.")
                break 

    print("Scraped")
        
    time.sleep(300)
