from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import uvicorn
import os
import traceback

# Import TwitterScraper with path adjustment
from utils.scrapper import TwitterScraper

# Mock DatabaseManager for now (you'll replace with actual implementation)
class DatabaseManager:
    def __init__(self):
        print("Initializing Database Manager")
    
    def save_trends(self, trends, ip_address):
        print(f"Saving trends for IP: {ip_address}")
        return {
            "trends_count": len(trends),
            "ip_address": ip_address,
            "timestamp": datetime.now().isoformat()
        }
    
    def close_connection(self):
        print("Closing database connection")

# Create FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (if you have a static directory)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Fallback if no static index.html
    return """
    <html>
        <head><title>Twitter Trends Scraper</title></head>
        <body>
            <h1>Twitter Trends Scraper</h1>
            <p>Use /scrape endpoint to fetch trending topics</p>
        </body>
    </html>
    """

@app.get("/scrape")
async def scrape_trends():
    scraper = None
    db = None
    try:
        # Initialize scraper and database
        scraper = TwitterScraper()
        db = DatabaseManager()
        
        # Get current IP
        ip_address = scraper.get_current_ip()
        if not ip_address:
            raise HTTPException(status_code=500, detail="Failed to get IP address")
        
        # Attempt login (this might be optional depending on your scraping strategy)
        # Uncomment if login is required
        # if not scraper.login():
        #     raise HTTPException(status_code=500, detail="Failed to login to Twitter")
        
        # Fetch trending topics
        trends = scraper.get_trending_topics()
        if not trends:
            raise HTTPException(status_code=500, detail="Failed to fetch trends")
        
        # Save trends to database
        record = db.save_trends(trends, ip_address)
        if not record:
            raise HTTPException(status_code=500, detail="Failed to save to database")
        
        # Return successful response
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "ip_address": ip_address,
            "trends": trends,
            "record": record
        }
    
    except Exception as e:
        # Detailed error logging
        print(f"Scraping error: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Ensure cleanup
        if scraper:
            try:
                scraper.cleanup()
            except Exception as cleanup_error:
                print(f"Error during scraper cleanup: {cleanup_error}")
        
        if db:
            try:
                db.close_connection()
            except Exception as db_error:
                print(f"Error closing database connection: {db_error}")

@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

# Entry point for running the application
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)