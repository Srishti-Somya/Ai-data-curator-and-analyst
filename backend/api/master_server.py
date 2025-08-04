# master_server.py
import sys
print(sys.path)

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import httpx

# Importing necessary functions from scrapping_modules_init and nlp_backend
import sys
sys.path.append('../nlp_processing')
from main import process_nlp
import sys
sys.path.append('../scraping_service')
# from parser import parser  # Commented out as parser.py doesn't exist

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cache = {}
class ScrapeRequest(BaseModel):
    query: str
    keywords: list
    columns_to_save: list
    
dummy_columns_to_save = [
    "Person",
    "Org",
    "Date",
    "Loc",
    "Misc",
    "Money",
    "Percent",
    "Time",
    "Quantity",
    "Ordinal",
    "Cardinal",
    "Product"
]

@app.post("/process")
async def process_request(request: ScrapeRequest):
        # Step 1: Call the scraper API and get filename of scraped data
    cache_key = (request.query, tuple(request.keywords))

        # Check if the result is already cached
    if cache_key in cache:
        print("Returning cached result for:", request)  # Log cache hit
        return cache[cache_key]  # Return cached result

    try:
        print("Received request:", request)  # Log the incoming request
            # Step 1: Call the scraper asynchronously and wait for the response
        url = "http://127.0.0.1:8001/scrape"
        data = {
                "query": request.query,
                "keyword": request.keywords
            }

        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.post(url, json=data)
            print("Response from scraper:", response.status_code, response.text)  # Log the response

            # Step 2: Check if the request was successful
        print("here")
        if response.status_code == 200:
            scrape_result = response.json()  # Expecting a JSON response with a filename
            print("Scrape successful:", scrape_result)
        else:
            print("Error:", response.status_code, response.text)
            raise HTTPException(status_code=response.status_code, detail=response.text)
        print("here1")
        # parser_instance = parser(request.keywords)  # Commented out as parser.py doesn't exist
        scraped_file_path = os.path.join("../data/scraped_data", scrape_result['filename'])
        parsed_file_path = scraped_file_path  # Use the scraped file directly
        
        # Process NLP
        print("here1")
        nlp_result = process_nlp(parsed_file_path, request.columns_to_save)
        
        return {
            "message": "Processing completed successfully",
            "csv_file": nlp_result["csv_file"],
            "svg_file": nlp_result["svg_file"],
            "entities_found": nlp_result["entities_found"],
            "data_rows": nlp_result["data_rows"]
        }
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in process_request: {e}")
        print(f"Full traceback: {error_details}")
        raise HTTPException(status_code=500, detail=f"Error during processing: {str(e)}")

@app.get("/svg")
async def get_svg_file():
    file_path = "relationships.svg"  # Direct path to the SVG file
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="image/svg+xml")
    raise HTTPException(status_code=404, detail="SVG file not found")

@app.get("/csv")
async def get_csv_file():
    file_path = "structured_data.csv"  # Direct path to the CSV file
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="text/csv")
    raise HTTPException(status_code=404, detail="CSV file not found")

@app.get("/files/svg/{filename}")
async def get_svg_file_by_name(filename: str):
    file_path = f"relationships/{filename}"  # Adjust path as needed
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="image/svg+xml")
    raise HTTPException(status_code=404, detail="SVG file not found")

@app.get("/files/csv/{filename}")
async def get_csv_file_by_name(filename: str):
    file_path = f"structured_data/{filename}"  # Adjust path as needed
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="text/csv")
    raise HTTPException(status_code=404, detail="CSV file not found")