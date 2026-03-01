from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from pydantic import BaseModel
from app.utils import generate_short_code
from dotenv import load_dotenv
import os
import sqlite3
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Database connection setup
@asynccontextmanager
async def lifespan(app: FastAPI):
    conn = sqlite3.connect('urls.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS urls
                    (id INTEGER PRIMARY KEY, short_code TEXT, original_url TEXT, clicks INTEGER)''')
    conn.commit()
    logger.info("Database initialized or already exists.")
    yield
    conn.close()
    logger.info("Database connection closed.")

app = FastAPI(lifespan=lifespan)

def get_db_connection():
    conn = sqlite3.connect('urls.db')
    return conn

class URLRequest(BaseModel):
    url: str

@app.get("/")
def home():
    logger.info("Home endpoint accessed.")
    return {"message": "URL Shortener API"}

@app.post("/shorten")
def shorten_url(request: URLRequest):
    logger.info(f"Request received to shorten URL: {request.url}")
    short_code = generate_short_code()
    conn = get_db_connection()

    while conn.execute("SELECT 1 FROM urls WHERE short_code = ?", (short_code,)).fetchone():
        short_code = generate_short_code()

    conn.execute("INSERT INTO urls (short_code, original_url, clicks) VALUES (?, ?, ?)",
                 (short_code, request.url, 0))
    conn.commit()
    conn.close()

    short_url = f"{os.getenv('BASE_URL', 'http://localhost:8000')}/{short_code}"
    logger.info(f"Shortened URL created: {short_url}")
    return {"short_url": short_url}

@app.get("/{short_code}")
def redirect_to_url(short_code: str):
    logger.info(f"Redirect request received for short_code: {short_code}")
    conn = get_db_connection()
    url_data = conn.execute("SELECT original_url, clicks FROM urls WHERE short_code = ?", (short_code,)).fetchone()

    if url_data is None:
        logger.warning(f"Shortened URL for {short_code} not found.")
        raise HTTPException(status_code=404, detail="Shortened URL not found")

    original_url, clicks = url_data
    conn.execute("UPDATE urls SET clicks = ? WHERE short_code = ?", (clicks + 1, short_code))
    conn.commit()
    conn.close()

    logger.info(f"Redirecting to {original_url}. Total clicks: {clicks + 1}")
    return RedirectResponse(url=original_url)