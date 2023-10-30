import openai
import os
import io
from dotenv import load_dotenv

import json
import requests

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
rapidapi_key = os.getenv("RAPIDAPI_KEY")

AUDIO_FORMATS = ['flac', 'm4a', 'mp3', 'mp4', 'mpeg', 'mpga', 'oga', 'ogg', 'wav', 'webm']

# Test function to check if api key is valid
def is_api_key_valid():
    try:
        response = openai.Completion.create(
            engine="davinci",
            prompt="This is a test.",
            max_tokens=5
        )
    except:
        return False
    else:
        return True


# Takes a request and gets chat gpt to respond
def text_request(user_in, type, api_key,file):

    # Checks for environment variables
    # If you have .env and an API key you don't need to manually insert
    # Otherwise, get from the website
    if(os.getenv("OPENAI_API_KEY")==None):
        openai.api_key = api_key

    # Check the key
    if(not is_api_key_valid()):
       return "Not a valid key"
    


    if(type == "text"):
        prompt = user_in

    elif(type == "youtube"):
        transcript = YouTubeTranscriptApi.get_transcript(user_in)
        formatter = TextFormatter()
        prompt = "Summarize this video transcript in 200 words" + formatter.format_transcript(transcript)[0:3500]
   
    elif(type == 'article'):
        apiurl = "https://news-article-extraction.p.rapidapi.com/"
        # payload = { "url": "https://edition.cnn.com/2020/06/30/tech/facebook-ad-business-boycott/index.html" }
        payload = { "url": user_in}
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": rapidapi_key,
            "X-RapidAPI-Host": "news-article-extraction.p.rapidapi.com"
        }

        res = requests.post(apiurl, json=payload, headers=headers)
        data = res.json()
        articleContent = data['content']
        prompt = 'summarize this article '+ articleContent

    # TODO add pdf/image/txt stuff
    if file != '':
        filetype = file.filename.rsplit('.',1)[1]
        a_file = io.BytesIO(file.read())
        a_file.name = file.filename
        if filetype == 'png':
            return 'png file'

            
        elif filetype in AUDIO_FORMATS:
            try:
                transcript = (openai.Audio.transcribe(model='whisper-1',file=a_file,response_format="text"))

            except:
                return "invalid audio file"

            return transcript

        elif filetype == 'txt':
            return file.read()

        elif filetype == 'pdf':
            return 'pdf file'


    # Test case without chatgpt request
    elif(type == 'test submit'):
        return "test submit"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt = prompt,
        temperature=0.6,
        max_tokens=200,
    )

    return(response.choices[0].text)
