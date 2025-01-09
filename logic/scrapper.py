from bs4 import BeautifulSoup
import time
from captcha_solver import solve_captcha

def call_url_and_solve(sb, link):
    sb.uc_open_with_reconnect(link)
    solve_captcha(sb)
    time.sleep(3)

def handle_next_page(sb, soup):
    """Handles the process of finding and opening the next page."""
    next_page_link = soup.find("li", class_="PagedList-skipToNext")
    if next_page_link:
        for retry_count in range(3):
            try:
                next_page_url = next_page_link.find("a")["href"]
                print(f"Going to next page: {next_page_url}")
                call_url_and_solve(sb, next_page_url)
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

def extract_title_link(item):
    title_tag = item.find("a", title=True)
    title = title_tag["title"] if title_tag else "Unknown Title"
    
    print(f"Title: {title}")
        
    link = title_tag["href"] if title_tag else "No Link"
    link = f"https://www.lightnovelcave.com{link}" if link.startswith("/") else link
    print(f"Link: {link}")

    figure_tag = item.find("figure", class_="novel-cover")
    image_tag = figure_tag.find("img") if figure_tag else None
    image_url = image_tag["src"] if image_tag else "No Image"
    print(f"Image Cover URL: {image_url}")
    time.sleep(1)
    return link

def extract_image(detail_soup):
    img_tag = detail_soup.find("img", class_="lazyloaded", alt=True)
    if img_tag:
        detail_image_url = img_tag["src"]
        print(f"Detail Image URL: {detail_image_url}")
    else:
        print("Image not found on the detail page.")

def extract_categories(detail_soup):
    categories_section = detail_soup.find("div", class_="categories")
    if categories_section:
        categories = categories_section.find_all("a", class_="property-item")
        print("Categories:")
        for category in categories:
            category_name = category.get_text(strip=True)
            print(f"- {category_name}")
    else:
        print("No categories found.")

def extract_summary(detail_soup):
    summary_section = detail_soup.find("div", class_="summary")
    if summary_section:
        paragraphs = summary_section.find_all("p")

        print("Summary:")
        for p in paragraphs:
            print(p.prettify())
    else:
        print("Summary section not found.")

def extract_tags(detail_soup):
    tags_section = detail_soup.find("div", class_="tags")
    if tags_section:

        li_elements = tags_section.find_all("li")
        
        tags = []
        for li in li_elements:
            a_tag = li.find("a", title=True)
            if a_tag:
                tag_title = a_tag["title"]
                tags.append(tag_title)
        
        print(tags)
    else:
        print("Tags section not found.")

def scrape(sb, url):

    call_url_and_solve(sb, url)  
    sb.set_messenger_theme(location="top_left")
    sb.post_message("SeleniumBase wasn't detected", duration=3)

    while True:
        page_source = sb.get_page_source()
        soup = BeautifulSoup(page_source, 'html.parser')

        novel_items = soup.find_all(class_="novel-item")

        for index, item in enumerate(novel_items, start=1):
            print(f"Novel {index}:")

            link = extract_title_link(item)
            print("-" * 80)
            
            try:
                print(f"Clicking on the link: {link}")
                call_url_and_solve(sb, link)

                page_source = sb.get_page_source()
                detail_soup = BeautifulSoup(page_source, 'html.parser')

                extract_image(detail_soup)
                extract_categories(detail_soup)
                extract_summary(detail_soup)
                extract_tags(detail_soup)

            except Exception as e:
                print(f"Error occurred while clicking the link: {e}")
                continue


        if not handle_next_page(sb, soup):
            break 

    print("Scraped")
        
    time.sleep(300)
