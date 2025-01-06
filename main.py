from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from utils.scrapper import TwitterScraper
from utils.db import DatabaseManager
from datetime import datetime
import uvicorn

app = FastAPI()
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html", "r") as f:
        return f.read()

@app.get("/scrape")
async def scrape_trends():
    scraper = None
    db = None
    try:
        scraper = TwitterScraper()
        db = DatabaseManager()
        
        ip_address = scraper.get_current_ip()
        if not ip_address:
            raise HTTPException(status_code=500, detail="Failed to get IP address")
            
        if not scraper.login():
            raise HTTPException(status_code=500, detail="Failed to login to Twitter")
            
        trends = scraper.get_trending_topics()
        try:
            print("Attempting to locate trends...")
            if not trends:
             raise HTTPException(status_code=500, detail="Failed to fetch trends")
    # Your scraping logic here
        except Exception as e:
            print(f"Error occurred while fetching trends: {e}")

            
        record = db.save_trends(trends, ip_address)
        if not record:
            raise HTTPException(status_code=500, detail="Failed to save to database")
            
        return {
            "success": True,
            "timestamp": datetime.now(),
            "ip_address": ip_address,
            "trends": trends,
            "record": record
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if scraper:
            scraper.cleanup()
        if db:
            db.close_connection()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)