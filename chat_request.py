import openai
import os
import io
from dotenv import load_dotenv

import json
import requests

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from PyPDF2 import PdfReader

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
def text_request(user_in,instructions,type,api_key,file,test_toggle):
    # Checks for environment variables
    # If you have .env and an API key you don't need to manually insert
    # Otherwise, get from the website
    if(os.getenv("OPENAI_API_KEY")==None):
        openai.api_key = api_key

    # Check the key
    if(not is_api_key_valid()):
       return "Not a valid key. Head to settings to change your OpenAI Key."

    if(instructions == ''):
        instructions = "Summarize this transcript in 200 words: "

    if(type == "text"):
        prompt = user_in

    elif(type == "youtube"):
        try:
            transcript = YouTubeTranscriptApi.get_transcript(user_in)
            formatter = TextFormatter()
            prompt = formatter.format_transcript(transcript)
        except:
            return "Invalid youtube id"
   
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

    elif(type == "audio file"):
        if file.filename == '':
            return "No file"

        filetype = file.filename.rsplit('.',1)[1]
        if filetype not in AUDIO_FORMATS:
            return "Invalid file type, must be " + str(AUDIO_FORMATS)

        a_file = io.BytesIO(file.read())
        a_file.name = file.filename

        prompt = openai.Audio.transcribe(model='whisper-1',file=a_file,response_format="text")

    elif("pdf/text file"):
        if file.filename == '':
            return "No file"

        filetype = file.filename.rsplit('.',1)[1]
        if filetype not in ["pdf","txt"]:
            return "Invalid file type, must be pdf or txt file"
        a_file = io.BytesIO(file.read())
        a_file.name = file.filename

        if filetype == 'txt':
            prompt = str(a_file.read())

        else:
            reader = PdfReader(a_file)
            prompt = ''
            for i in reader.pages:
                prompt += i.extract_text()



    # Test case without chatgpt request
    if test_toggle:
        return instructions + prompt
    

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content":instructions + prompt[0:10000]}
        ]
    )

    return response.choices[0].message["content"]