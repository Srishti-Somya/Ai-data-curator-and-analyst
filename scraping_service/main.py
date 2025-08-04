# scrapping_modules_init/main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from collections import deque
import datetime
import os
from query import google_search
from scrapper import scrape_page, save_to_txt, dataset, visited_urls
import time

# Ensure the app instance is correctly defined
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request body model for scraping
class ScrapeRequest(BaseModel):
    query: str  # Search query
    keyword: list  # Keywords for scraping

cache = {}

@app.post("/scrape")
async def scrape_content(request: ScrapeRequest):
    print(f"\n=== SCRAPING REQUEST ===")
    print(f"Query: {request.query}")
    print(f"Keywords: {request.keyword}")
    
    try:
        # Clear previous data
        dataset.clear()
        visited_urls.clear()
        
        # Get URLs from search
        urls = google_search(request.query, request.keyword)
        print(f"Found {len(urls)} URLs to scrape")
        
        if not urls:
            raise HTTPException(status_code=404, detail="No URLs found")
        
        # Crawl with increased depth and page limit
        url_queue = deque([(url, 0) for url in urls])
        max_depth = 2  # Reduced from 3 to 2 for faster processing
        max_pages = 15  # Increased from 10 to 15 for more content
        
        print(f"Starting crawl with max_depth={max_depth}, max_pages={max_pages}")
        
        while url_queue and len(dataset) < max_pages:
            url, depth = url_queue.popleft()
            
            if depth > max_depth:
                continue
                
            print(f"\nProcessing URL {len(dataset) + 1}/{max_pages}: {url}")
            scrape_page(url, depth, request.keyword, url_queue)
            
            # Add small delay to be respectful
            time.sleep(0.5)  # Reduced delay for faster processing
        
        print(f"\nCrawling completed. Total pages scraped: {len(dataset)}")
        
        if not dataset:
            raise HTTPException(status_code=404, detail="No relevant content found")
        
        # Save to file
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"dataset_{timestamp}.txt"
        file_path = save_to_txt(dataset, filename)
        
        print(f"Data saved to: {file_path}")
        print(f"Total content length: {sum(len(item['content']) for item in dataset)} characters")
        
        return {
            "message": "Scraping completed successfully",
            "filename": filename,
            "pages_scraped": len(dataset),
            "total_content_length": sum(len(item['content']) for item in dataset),
            "urls": [item['url'] for item in dataset]
        }
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error during scraping: {e}")
        print(f"Full traceback: {error_details}")
        raise HTTPException(status_code=500, detail=f"Error during scraping: {str(e)}")
