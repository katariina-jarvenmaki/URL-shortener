# URL-shortener
URL-shortener project to showcase python use

## Create venv
cd /opt/kjc/int/URL-shortener
python3 -m venv venv
source venv/bin/activate

## Run locally
```bash
uvicorn app.main:app --reload
```
Then check: 
http://127.0.0.1:8000 
http://127.0.0.1:8000/docs

Test Short URL Endpoint
http://127.0.0.1:8000/shorten