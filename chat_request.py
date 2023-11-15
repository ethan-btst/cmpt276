import openai
from openai import OpenAI
import os
import io
from dotenv import load_dotenv

import json
import requests

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from PyPDF2 import PdfReader

load_dotenv()

rapidapi_key = os.getenv("RAPIDAPI_KEY")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)
AUDIO_FORMATS = ['flac', 'm4a', 'mp3', 'mp4', 'mpeg', 'mpga', 'oga', 'ogg', 'wav', 'webm']


# Test function to check if api key is valid
def not_valid_key():
    try:
        response = client.completions.create(engine="davinci",
        prompt="This is a test.",
        max_tokens=5)
    except:
        print('invalid key')
        return True
    else:
        print('valid key')
        return False

# Prompt generators
def youtube_prompt(link):
    transcript = YouTubeTranscriptApi.get_transcript(link)
    formatter = TextFormatter()
    return formatter.format_transcript(transcript)

def article_prompt(link):
    apiurl = "https://news-article-extraction.p.rapidapi.com/"
    # payload = { "url": "https://edition.cnn.com/2020/06/30/tech/facebook-ad-business-boycott/index.html" }
    payload = { "url": link}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": rapidapi_key,
        "X-RapidAPI-Host": "news-article-extraction.p.rapidapi.com"
    }

    res = requests.post(apiurl, json=payload, headers=headers)
    data = res.json()
    articleContent = data['content']
    return articleContent
    
def audio_prompt(file):
    if file.filename == '':
        return "No file"

    filetype = file.filename.rsplit('.',1)[1]
    if filetype not in AUDIO_FORMATS:
        return "Invalid file type, must be " + str(AUDIO_FORMATS)

    a_file = io.BytesIO(file.read())
    a_file.name = file.filename

    return client.audio.transcriptions.create(
        model="whisper-1", 
        file=a_file, 
        response_format="text"
    )

def pdf_text_prompt(file):
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

    return prompt


# Takes a request and gets chat gpt to respond
def text_request(user_in,instructions,type,api_key,file,test_toggle):

    if(instructions == ''):
        instructions = "Summarize this in 200 words: "

    if(type == "text"):
        prompt = user_in

    elif(type == "youtube"):
        try:
            prompt = youtube_prompt(user_in)
        except:
            return "Invalid youtube id"
   
    elif(type == 'article'):
        try:
            prompt = article_prompt(user_in)
        except:
            return "Invalid link"

    elif(type == "audio file"):
        prompt = audio_prompt(file)

    elif("pdf/text file"):
        prompt = pdf_text_prompt(file)

    # Test case without chatgpt request
    if test_toggle:
        return instructions + prompt
    
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
        {"role": "user", "content":instructions + prompt[0:10000]}
        ])
    
    except:
        return "Sorry, something went wrong"

    return response.choices[0].message.content