from bs4 import BeautifulSoup
import time
from captcha_solver import solve_captcha

def handle_next_page(sb, soup):
    """Handles the process of finding and opening the next page."""
    next_page_link = soup.find("li", class_="PagedList-skipToNext")
    if next_page_link:
        for retry_count in range(3):
            try:
                next_page_url = next_page_link.find("a")["href"]
                print(f"Going to next page: {next_page_url}")
                sb.uc_open_with_reconnect(next_page_url)
                solve_captcha(sb)
                time.sleep(3)
                return True
            except Exception as e:
                print(f"Error occurred: {e}. Retrying...")
                time.sleep(2)
        else:
            print("No more retries, exiting scraping.")
            return False
    else:
        print("No more pages to scrape.")
        return False

def scrape(sb, url):
    sb.uc_open_with_reconnect(url)
    solve_captcha(sb)
    
    sb.set_messenger_theme(location="top_left")
    sb.post_message("SeleniumBase wasn't detected", duration=3)

    while True:
        page_source = sb.get_page_source()
        soup = BeautifulSoup(page_source, 'html.parser')

        novel_items = soup.find_all(class_="novel-item")

        for index, item in enumerate(novel_items, start=1):
            print(f"Novel {index}:")

            title_tag = item.find("a", title=True)
            title = title_tag["title"] if title_tag else "Unknown Title"

            link = title_tag["href"] if title_tag else "No Link"
            link = f"https://www.lightnovelcave.com{link}" if link.startswith("/") else link

            figure_tag = item.find("figure", class_="novel-cover")
            image_tag = figure_tag.find("img") if figure_tag else None
            image_url = image_tag["src"] if image_tag else "No Image"

            print(f"Title: {title}")
            time.sleep(1)

            print(f"Link: {link}")
            time.sleep(1)

            print(f"Image URL: {image_url}")
            time.sleep(1)

            print("-" * 80)
            try:
                print(f"Clicking on the link: {link}")
                sb.uc_open_with_reconnect(link)
                solve_captcha(sb)
                time.sleep(3)

                page_source = sb.get_page_source()
                detail_soup = BeautifulSoup(page_source, 'html.parser')

                img_tag = detail_soup.find("img", class_="lazyloaded", alt=True)
                if img_tag:
                    detail_image_url = img_tag["src"]
                    print(f"Detail Image URL: {detail_image_url}")
                else:
                    print("Image not found on the detail page.")
                time.sleep(2)

                categories_section = detail_soup.find("div", class_="categories")
                if categories_section:
                    categories = categories_section.find_all("a", class_="property-item")
                    print("Categories:")
                    for category in categories:
                        category_name = category.get_text(strip=True)
                        print(f"- {category_name}")
                else:
                    print("No categories found.")

            except Exception as e:
                print(f"Error occurred while clicking the link: {e}")
                continue


        if not handle_next_page(sb, soup):
            break 

    print("Scraped")
        
    time.sleep(300)
