from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
from selenium.webdriver.chrome.options import Options
import platform

def create_chrome_driver():
    """Create a new Chrome WebDriver instance with robust configuration"""
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Use selenium-manager to automatically download the correct ChromeDriver
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Set page load timeout
        driver.set_page_load_timeout(30)
        driver.implicitly_wait(10)
        
        return driver
    except Exception as e:
        print(f"Error creating Chrome driver: {e}")
        print("Falling back to direct website crawling...")
        return None

# Global driver variable
driver = None

def get_driver():
    """Get or create a Chrome WebDriver instance"""
    global driver
    try:
        if driver is None:
            driver = create_chrome_driver()
        # Test if driver is still responsive
        driver.current_url
        return driver
    except Exception as e:
        print(f"Driver not responsive, creating new one: {e}")
        try:
            if driver:
                driver.quit()
        except:
            pass
        driver = create_chrome_driver()
        return driver

# Google search
def google_search(query, keywords):
    print(f"\nPerforming web search for query: {query}")
    print(f"Keywords: {keywords}")
    search_query = f"{query} {' '.join(keywords)}"  # Simplified search query
    print(f"Full search query: {search_query}")
    
    try:
        # Get a fresh driver instance
        driver = get_driver()
        if not driver:
            print("Failed to create WebDriver, using direct website crawling")
            return crawl_direct_websites(query, keywords)
        
        # Try multiple search engines
        search_engines = [
            ("https://www.bing.com/search?q=", "li.b_algo h2 a"),
            ("https://duckduckgo.com/?q=", "h2 a"),
            ("https://www.google.com/search?q=", "div.g a")
        ]
        
        search_results = []
        for engine_url, selector in search_engines:
            try:
                print(f"Trying search engine: {engine_url}")
                driver.get(f"{engine_url}{search_query}")
                print("Search page loaded")
                
                # Handle cookie consent if present
                try:
                    cookie_button = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'I agree') or contains(text(), 'Allow')]"))
                    )
                    cookie_button.click()
                    print("Accepted cookies")
                except:
                    print("No cookie consent found or already accepted")
                
                time.sleep(3)  # Wait for results to load
                
                # Try to find search results
                search_results = driver.find_elements(By.CSS_SELECTOR, selector)
                if search_results:
                    print(f"Found {len(search_results)} results using selector: {selector}")
                    break
                else:
                    print(f"No results found with selector: {selector}")
                    
            except Exception as e:
                print(f"Error with search engine {engine_url}: {e}")
                continue
        
        if not search_results:
            print("No search results found from any search engine")
            # Try direct website crawling based on keywords
            return crawl_direct_websites(query, keywords)
        
        urls = []
        for index, result in enumerate(search_results[:5]):  #first 5 for eg
            try:
                url = result.get_attribute("href")
                if url and url.startswith('http') and not any(domain in url for domain in ['google.com', 'bing.com', 'duckduckgo.com']):
                    urls.append(url)
                    print(f"Result {index + 1}: {url}")
            except Exception as e:
                print(f"Error extracting URL from result {index + 1}: {e}")

        print(f"Successfully extracted {len(urls)} URLs")
        return urls
        
    except Exception as e:
        print(f"Error during web search: {e}")
        # Try direct website crawling as fallback
        return crawl_direct_websites(query, keywords)

def crawl_direct_websites(query, keywords):
    """Crawl relevant English websites directly based on keywords"""
    print("Attempting direct website crawling for English content...")
    
    # Define relevant English websites based on keywords
    websites = []
    
    # Climate/Environment related
    if any(word in query.lower() for word in ['climate', 'environment', 'renewable', 'carbon', 'energy']):
        websites = [
            "https://www.un.org/en/climatechange",
            "https://www.epa.gov/climate-change", 
            "https://www.nationalgeographic.com/environment/topic/climate-change",
            "https://www.climate.gov/",
            "https://www.ipcc.ch/",
            "https://www.bbc.com/news/science-environment",
            "https://www.theguardian.com/environment"
        ]
    # Technology/AI related
    elif any(word in query.lower() for word in ['ai', 'artificial intelligence', 'machine learning', 'technology']):
        websites = [
            "https://www.technologyreview.com/",
            "https://www.wired.com/",
            "https://www.theverge.com/",
            "https://www.techcrunch.com/",
            "https://www.artificialintelligence-news.com/",
            "https://www.bbc.com/news/technology",
            "https://www.theguardian.com/technology",
            "https://www.nytimes.com/section/technology"
        ]
    # Programming related
    elif any(word in query.lower() for word in ['python', 'programming', 'code', 'software']):
        websites = [
            "https://www.python.org/",
            "https://docs.python.org/3/tutorial/",
            "https://realpython.com/",
            "https://www.geeksforgeeks.org/python-programming-language/",
            "https://www.tutorialspoint.com/python/",
            "https://www.w3schools.com/python/",
            "https://www.programiz.com/python-programming"
        ]
    # Space/Science related
    elif any(word in query.lower() for word in ['space', 'nasa', 'mars', 'satellite', 'astronomy']):
        websites = [
            "https://www.nasa.gov/",
            "https://www.space.com/",
            "https://www.esa.int/",
            "https://www.bbc.com/news/science-environment",
            "https://www.science.org/",
            "https://www.nature.com/"
        ]
    # General knowledge
    else:
        websites = [
            "https://www.wikipedia.org/",
            "https://www.britannica.com/",
            "https://www.encyclopedia.com/",
            "https://www.bbc.com/news",
            "https://www.theguardian.com/",
            "https://www.nytimes.com/"
        ]
    
    print(f"Will crawl {len(websites)} English websites: {websites}")
    return websites

def get_user_input(q):
    query = input("Enter your query: ")
    keywords = []
    for i in range(4):
        keyword = input(f"Enter keyword {i+1}: ")
        keywords.append(keyword)
    q.put((query, keywords))

# def main():
#     q = queue.Queue()
#     # Create a new thread to get the user input
#     input_thread = threading.Thread(target=get_user_input, args=(q,))
#     input_thread.start()
#     input_thread.join()
#     query, keywords = q.get()
#     urls = google_search(query, keywords)
#     return urls, keywords

# if __name__ == "__main__":
#     main()