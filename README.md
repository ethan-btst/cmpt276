# CMPT 276 project

## Setup locally
1. Clone repository to your system and enter it
```
git clone https://github.com/ethan-btst/cmpt276.git
cd cmpt276
```

2. Set up the virtual environment using:
```
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
flask run
```
2. Or when debugging (So you don't have to restart flask server after changes):
```
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
flask --app app.py --debug run
```


3. Create the '.env' for the your api key
   
   In .env put:
   > OPENAI_API_KEY = _your api key_
   RAPIDAPI_KEY = _your_api_key_

