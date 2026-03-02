# URL-shortener
URL-shortener project to showcase python use

## Create venv
```bash
cd /opt/kjc/int/URL-shortener
python3 -m venv venv
source venv/bin/activate
```

## Run locally
```bash
uvicorn app.main:app --reload
```
Then check:<br> 
http://127.0.0.1:8000<br>
http://127.0.0.1:8000/docs

Test Short URL Endpoint:<br>
http://127.0.0.1:8000/shorten

## Running a test
```bash
PYTHONPATH=./ pytest
export PYTHONPATH=$(pwd)
pytest
 ```