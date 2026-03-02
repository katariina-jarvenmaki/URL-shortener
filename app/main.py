from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from app.utils import generate_short_code
from pydantic import BaseModel, HttpUrl
from pydantic_settings import BaseSettings
import sqlite3
import logging

class AppSettings(BaseSettings):
    base_url: str = "http://localhost:8000"
    database_url: str = "urls.db"

settings = AppSettings()  # Load environment variables

# Set up logging configuration
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Database connection setup
@asynccontextmanager
async def lifespan(app: FastAPI):
    conn = sqlite3.connect(settings.database_url)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY,
        short_code TEXT UNIQUE,
        original_url TEXT NOT NULL,
        clicks INTEGER DEFAULT 0
    );
    """)
    conn.execute("""
    CREATE INDEX IF NOT EXISTS idx_short_code ON urls(short_code);
    """)
    conn.commit()
    logger.info("Database initialized or already exists.")
    yield
    conn.close()
    logger.info("Database connection closed.")

app = FastAPI(lifespan=lifespan)

def get_db_connection():
    return sqlite3.connect(settings.database_url, check_same_thread=False)

class URLRequest(BaseModel):
    url: HttpUrl

@app.get("/")
def home():
    logger.info("Home endpoint accessed.")
    return {"message": "URL Shortener API"}

@app.post("/shorten")
def shorten_url(request: URLRequest):
    conn = get_db_connection()

    existing = conn.execute(
        "SELECT short_code FROM urls WHERE original_url = ?",
        (str(request.url),)
    ).fetchone()

    if existing:
        conn.close()
        return {"short_url": f"{settings.base_url}/{existing[0]}"}

    short_code = generate_short_code()
    while conn.execute(
        "SELECT 1 FROM urls WHERE short_code = ?",
        (short_code,)
    ).fetchone():
        short_code = generate_short_code()

    conn.execute(
        "INSERT INTO urls (short_code, original_url, clicks) VALUES (?, ?, 0)",
        (short_code, str(request.url))
    )
    conn.commit()
    conn.close()

    return {"short_url": f"{settings.base_url}/{short_code}"}

@app.get("/{short_code}")
def redirect_to_url(short_code: str):
    conn = get_db_connection()
    url_data = conn.execute(
        "SELECT original_url FROM urls WHERE short_code = ?",
        (short_code,)
    ).fetchone()

    if url_data is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Shortened URL not found")

    original_url = url_data[0]

    conn.execute(
        "UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?",
        (short_code,)
    )
    conn.commit()
    conn.close()

    return RedirectResponse(url=original_url)

@app.get("/stats/{short_code}")
def get_url_stats(short_code: str):
    logger.info(f"Stats request received for short_code: {short_code}")
    conn = get_db_connection()
    url_data = conn.execute("SELECT original_url, clicks FROM urls WHERE short_code = ?", (short_code,)).fetchone()
    
    if url_data is None: 
        logger.warning(f"Stats not found for {short_code}.")
        conn.close()
        raise HTTPException(status_code=404, detail="URL stats not found")
        
    original_url, clicks = url_data
    
    conn.close()
    
    logger.info(f"Returning stats for {original_url}. Total clicks: {clicks}")
    
    return {"original_url": original_url, "clicks": clicks}