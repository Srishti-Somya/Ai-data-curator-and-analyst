from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
from urllib.parse import urljoin, urlparse
from collections import deque
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
from query import get_driver  # Use the improved driver management

# Set up Selenium WebDriver
wait = WebDriverWait(get_driver(), 10)
visited_urls = set()
dataset = []

def is_english_text(text, threshold=0.7):
    """
    Check if text is primarily English by counting ASCII characters.
    Returns True if more than threshold% of characters are ASCII.
    """
    if not text:
        return False
    
    ascii_count = sum(1 for char in text if ord(char) < 128)
    total_count = len(text)
    
    if total_count == 0:
        return False
    
    english_ratio = ascii_count / total_count
    return english_ratio >= threshold

def extract_useful_content(soup):
    print("Extracting content from soup...")
    useful_content = ""
    
    # Remove script and style elements
    for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
        script.decompose()
    
    # Try finding main content in typical HTML tags
    main_content_selectors = [
        'main', 'article', 'div[role="main"]', '.main-content', '.content', 
        '.post-content', '.entry-content', '.article-content', 'body'
    ]
    
    main_content = None
    for selector in main_content_selectors:
        main_content = soup.select_one(selector)
        if main_content:
            print(f"Found main content using selector: {selector}")
            break
    
    if main_content:
        # Extract paragraphs with more content
        paragraphs = main_content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        print(f"Found {len(paragraphs)} text elements")
        
        english_paragraphs = []
        for element in paragraphs:
            text = element.get_text().strip()
            if len(text) > 20 and is_english_text(text):  # Only include substantial English text
                english_paragraphs.append(text)
                useful_content += text + "\n\n"
        
        # Extract list items (if any)
        lists = main_content.find_all(['ul', 'ol'])
        print(f"Found {len(lists)} lists")
        for lst in lists:
            items = lst.find_all('li')
            for item in items:
                text = item.get_text().strip()
                if len(text) > 10 and is_english_text(text):
                    useful_content += "- " + text + "\n"
            useful_content += "\n"
    else:
        print("No main content found, using entire body")
        full_text = soup.get_text()
        # Filter for English content only
        lines = full_text.split('\n')
        english_lines = [line.strip() for line in lines if len(line.strip()) > 10 and is_english_text(line.strip())]
        useful_content = '\n'.join(english_lines)
    
    # Clean up the content
    import re
    # Remove excessive whitespace
    useful_content = re.sub(r'\n\s*\n', '\n\n', useful_content)
    # Remove very short lines
    lines = useful_content.split('\n')
    cleaned_lines = [line.strip() for line in lines if len(line.strip()) > 10 and is_english_text(line.strip())]
    useful_content = '\n'.join(cleaned_lines)
    
    content = useful_content.strip()
    print(f"Extracted content length: {len(content)}")
    print(f"Content preview: {content[:200]}...")
    
    # Check if we have enough English content
    if len(content) < 50:  # Reduced from 100 to 50
        print("Warning: Very little English content found")
        return ""
    
    return content

def save_to_txt(data, filename='dataset.txt'):
    print(f"Saving data to {filename}...")
    output_dir = "../data/scraped_data/"
    # Create directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    full_path = output_dir + filename
    print(f"Full path: {full_path}")
    print(f"Number of items to save: {len(data)}")
    
    try:
        with open(full_path, 'w', encoding='utf-8') as file:
            for item in data:
                file.write(f"URL: {item['url']}\n")
                file.write("="*50 + "\n")
                file.write(item['content'] + "\n\n")
                file.write("-"*50 + "\n\n")
        print("Data saved successfully")
        return full_path
    except Exception as e:
        print(f"Error saving data: {e}")
        raise

def interact_with_ui(driver):
    print("Interacting with UI elements...")
    try:
        expand_buttons = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'collapsible')))
        print(f"Found {len(expand_buttons)} expandable sections")
        for button in expand_buttons:
            try:
                driver.execute_script("arguments[0].click();", button)
                time.sleep(1)  # Reduced wait time
            except Exception as e:
                print(f"Error clicking button: {e}")
    except TimeoutException:
        print("No expandable sections found")
    except Exception as e:
        print(f"Error in UI interaction: {e}")

def scrape_page(url, depth, keywords, url_queue):
    print(f"\nScraping page: {url}")
    if url in visited_urls:
        print("URL already visited, skipping")
        return
    
    visited_urls.add(url)
    print(f"Total visited URLs: {len(visited_urls)}")
    
    try:
        driver = get_driver()
        if driver is None:
            # Fallback to requests when ChromeDriver is not available
            print("ChromeDriver not available, using requests fallback...")
            import requests
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
        else:
            print("Loading page with Chrome WebDriver...")
            driver.get(url)
            print("Page loaded successfully")

            # UI interaction with retry
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    interact_with_ui(driver)
                    break
                except Exception as e:
                    print(f"UI interaction attempt {attempt + 1} failed: {e}")
                    if attempt == max_retries - 1:
                        print("All UI interaction attempts failed")

            print("Parsing page with BeautifulSoup...")
            soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        content = extract_useful_content(soup)
        
        print(f"Content preview (first 200 chars): {content[:200]}...")
        print(f"Keywords to search for: {keywords}")
        
        # More lenient content acceptance - include more content for better entity extraction
        has_keywords = any(keyword.lower() in content.lower() for keyword in keywords)
        has_substantial_content = len(content.strip()) > 20  # Reduced threshold for more content
        
        print(f"Has keywords: {has_keywords}")
        print(f"Has substantial content: {has_substantial_content}")
        print(f"Content length: {len(content)}")
        
        # Accept content if it has substantial text, even without keywords
        if has_substantial_content:
            print("Content meets criteria - adding to dataset")
            dataset.append({'url': url, 'content': content})
            print(f"Total items in dataset: {len(dataset)}")
            
            # Store more relevant links for comprehensive crawling
            links = soup.find_all('a', href=True)
            print(f"Found {len(links)} links on page")
            added_links = 0
            for link in links:
                try:
                    link_url = urljoin(url, link['href'])
                    link_text = link.get_text().strip()
                    
                    # More comprehensive link filtering
                    if (urlparse(link_url).netloc == urlparse(url).netloc and 
                        link_url not in visited_urls and 
                        len(link_text) > 0 and
                        not any(skip in link_url.lower() for skip in ['#', 'javascript:', 'mailto:', 'tel:'])):
                        print(f"Adding link to queue: {link_url}")
                        url_queue.append((link_url, depth + 1))
                        added_links += 1
                        if added_links >= 5:  # Increased from 3 to 5 for more comprehensive crawling
                            break
                except Exception as e:
                    print(f"Error processing link: {e}")
            print(f"Added {added_links} links to queue")
        else:
            print("Content does not meet criteria - skipping")
    except TimeoutException as e:
        print(f"Timeout error scraping {url}: {e}")
    except WebDriverException as e:
        print(f"WebDriver error scraping {url}: {e}")
    except Exception as e:
        print(f"Unexpected error scraping {url}: {e}")
    finally:
        try:
            driver = get_driver()
            if driver:
                driver.execute_script("window.stop();")
        except:
            pass
