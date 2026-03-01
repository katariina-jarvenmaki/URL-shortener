from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.get("/")
def home():
    return {"message": "URL Shortener API"}
    