from bs4 import BeautifulSoup
import time
from captcha_solver import trigger_capcha
import re
from insert.insert import insert_novel, insert_chapter, update_last_chapter
from checker.checker import get_last_chapter
from alter.updater import update_subchapters
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def call_url_and_solve(sb, link):
    sb.get(link)
    trigger_capcha(sb)

def handle_next_page(sb, soup):
    """Handles the process of finding and opening the next page."""
    next_page_link = soup.find("li", class_="PagedList-skipToNext")
    if next_page_link:
        for retry_count in range(3):
            try:
                next_page_url = next_page_link.find("a")["href"]
                print(f"Going to next page: {next_page_url}")
                
                WebDriverWait(sb, 30).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "li.PagedList-skipToNext a"))
                )
                
                call_url_and_solve(sb, next_page_url)
                return True
            except Exception as e:
                print(f"Error occurred: {e}. Retrying...")
                time.sleep(1)
        else:
            print("retrigger handle next page")
            handle_next_page(sb, soup)
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

    return link, title

def extract_image(detail_soup):
    img_tag = detail_soup.find("img", class_="lazyloaded", alt=True)
    if img_tag:
        detail_image_url = img_tag["src"]
        print(f"Detail Image URL: {detail_image_url}")
        return detail_image_url
    else:
        print("Image not found on the detail page.")

def extract_categories(detail_soup):
    categories_section = detail_soup.find("div", class_="categories")
    if categories_section:
        categories = categories_section.find_all("a", class_="property-item")
        print("Categories:")
        category_list = [category.get_text(strip=True) for category in categories]
        print(category_list)
        return category_list
    else:
        return []
        print("No categories found.")

def extract_summary(detail_soup):
    summary_section = detail_soup.find("div", class_="summary")
    if summary_section:
        paragraphs = summary_section.find_all("p")

        print("Summary:")
        all_paragraphs = "".join(str(p) for p in paragraphs)

        print(all_paragraphs)
        return all_paragraphs
    else:
        print("Summary section not found.")
        return ""

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
        return tags
    else:
        print("Tags section not found.")

def extract_author(detail_soup):
    author = detail_soup.find('span', {'itemprop': 'author'})
    if author:
        print(author.text)
        return author.text

def navigate_to_chapters(detail_soup):
    link = detail_soup.find("a", class_="grdbtn chapter-latest-container")
    href = link.get("href") if link else None
    return f"https://www.lightnovelcave.com{href}" if href and href.startswith("/") else href

def navigate_to_first_chapter(chapter_soup, novel_id):
    last_chapter = get_last_chapter(novel_id)
    link = chapter_soup.select_one("ul.chapter-list li a")
    href = link["href"] if link else None

    absolute_href = f"https://www.lightnovelcave.com{href}" if href and href.startswith("/") else href
    if last_chapter is None:
        return absolute_href

    if "chapter-" in absolute_href:
        new_href = re.sub(r"(chapter-\d+).*", f"chapter-{last_chapter}", absolute_href)
        return new_href
            
    return absolute_href


def navigate_next_chapter(soup):
    anchor_tag = soup.find('a', class_='button nextchap')
    href = anchor_tag['href'] if anchor_tag else None
    return f"https://www.lightnovelcave.com{href}" if href and href.startswith("/") else href

def extract_chapter(chapter):
    title_tag = chapter.select_one('span.chapter-title')
    title = title_tag.text if title_tag else None

    p_tags = chapter.select('#chapter-container p')
    content = "".join(str(p) for p in p_tags)
        
    return title, content

def process_chapters(sb, chapter, novel_id):
    attempts = 0
    while chapter:
        try:
            print(f"Clicking on the chapter: {chapter}")
   
            call_url_and_solve(sb, chapter)
            page_source = sb.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            chapter_title, content = extract_chapter(soup)

            match = re.search(r'chapter-(\d+)', chapter)
            if match:
                chapter_number = match.group(1)
                print(f"Extracted chapter number: {chapter_number}")
                chapter_result = insert_chapter(novel_id, chapter_title, content, chapter_number)
                if chapter_result is None:
                    print(f"Failed to insert chapter or Chapter Already exist {chapter_number}. Exiting loop.")
                    attempts +=1
                    if attempts >= 5:
                        print(f"Second page is duplicate chapter {chapter_number}. Exiting loop.")
                        attempts = 0
                        break
                else:
                    attempts = 0
                    update_last_chapter(novel_id, chapter_number)

            next_chapter_url = navigate_next_chapter(soup)          

            if next_chapter_url:
                chapter = f"{next_chapter_url}"
                print(f"Next chapter found, moving to: {chapter}")
            else:
                print("No more chapters found. Exiting loop.")
                break

        except Exception as e:
            print(f"Error occurred while clicking the link: {e}")
            continue

def scrape(sb, url):

    call_url_and_solve(sb, url)  
    sb.save_screenshot("screenshot.png")
    print()
    while True:
        page_source = sb.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        novel_items = soup.find_all(class_="novel-item")

        for index, item in enumerate(novel_items, start=1):
            print(f"Novel {index}:")

            link, title = extract_title_link(item)
            print("-" * 80)


            try:
                print(f"Clicking on the link: {link}")
                call_url_and_solve(sb, link)

                page_source = sb.page_source
                detail_soup = BeautifulSoup(page_source, 'html.parser')

                image = extract_image(detail_soup)
                categories = extract_categories(detail_soup)
                summary = extract_summary(detail_soup)
                tags = extract_tags(detail_soup)
                author = extract_author(detail_soup)
                insert_novel(image, title, summary, author, categories, tags)
                # novel_id = insert_novel(image, title, summary, author, categories, tags)
                # chapter_link = navigate_to_chapters(detail_soup)
                # try:
                #     print(f"Clicking on the chapter_link: {chapter_link}")
                #     call_url_and_solve(sb, chapter_link)
                #     page_source = sb.page_source
                #     chapter_soup = BeautifulSoup(page_source, 'html.parser')
                #     chapter = navigate_to_first_chapter(chapter_soup, novel_id)
                #     print(f"Chapter go to {chapter}")
                #     print(f"novel_id go to {novel_id}")
                #     process_chapters(sb, chapter, novel_id)
                
                # except Exception as e:
                #     print(f"Error occurred while clicking the link: {e}")
                #     continue

            except Exception as e:
                print(f"Error occurred while clicking the link: {e}")
                continue


        if not handle_next_page(sb, soup):
            break 
    update_subchapters()
    print("Scraped")