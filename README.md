# CMPT 276 Media Summary App

## Setup locally

1. Clone repository to your system and enter it

```
git clone https://github.com/ethan-btst/cmpt276.git
cd cmpt276
```

2. Option a. Set up the virtual environment using:

```
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
flask run
```

2. Option b. Or when debugging (So you don't have to restart flask server after changes):

- Also be sure to clear cookies (or test incognito) cause login cookies may be saved (Especially when trying to debug not logged in cases)

```
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
flask --app app.py --debug run
```

3. Create the '.env' for the your api key

   In .env put:

   > OPENAI*API_KEY = \_your api key*
   > RAPIDAPI*KEY = \_your_api_key*
   > DATABASE*URL = \_your_postgres-elephant_url*

## Things to keep in mind - Testing (May be moved to another doc file later)

- When adding routes, making sure to prevent keyerrors and unwanted access-redirects
