from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from app.utils import generate_short_code
from dotenv import load_dotenv
import os
import sqlite3
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    conn = sqlite3.connect('urls.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS urls
                    (id INTEGER PRIMARY KEY, short_code TEXT, original_url TEXT, clicks INTEGER)''')
    conn.commit()
    yield
    conn.close()

app = FastAPI(lifespan=lifespan)

def get_db_connection():
    conn = sqlite3.connect('urls.db')
    return conn

class URLRequest(BaseModel):
    url: str

@app.get("/")
def home():
    return {"message": "URL Shortener API"}

@app.post("/shorten")
def shorten_url(request: URLRequest):
    short_code = generate_short_code()
    conn = get_db_connection()

    while conn.execute("SELECT 1 FROM urls WHERE short_code = ?", (short_code,)).fetchone():
        short_code = generate_short_code()

    conn.execute("INSERT INTO urls (short_code, original_url, clicks) VALUES (?, ?, ?)",
                 (short_code, request.url, 0))
    conn.commit()
    conn.close()

    return {"short_url": f"{os.getenv('BASE_URL', 'http://localhost:8000')}/{short_code}"}

@app.get("/{short_code}")
def redirect_to_url(short_code: str):
    conn = get_db_connection()
    url_data = conn.execute("SELECT original_url, clicks FROM urls WHERE short_code = ?", (short_code,)).fetchone()

    if url_data is None:
        raise HTTPException(status_code=404, detail="Shortened URL not found")

    original_url, clicks = url_data
    conn.execute("UPDATE urls SET clicks = ? WHERE short_code = ?", (clicks + 1, short_code))
    conn.commit()
    conn.close()

    return RedirectResponse(url=original_url)