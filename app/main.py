from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from app.utils import generate_short_code

app = FastAPI()

url_store = {}

class URLRequest(BaseModel):
    url: str

@app.get("/")
def home():
    return {"message": "URL Shortener API"}

@app.post("/shorten")
def shorten_url(request: URLRequest):
    short_code = generate_short_code()

    url_store[short_code] = {
        "original_url": request.url,
        "clicks": 0
    }

    return {"short_url": f"http://localhost:8000/{short_code}"}