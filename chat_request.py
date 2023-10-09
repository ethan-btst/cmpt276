import openai
import os
from dotenv import load_dotenv

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

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

def text_request(user_in, type,api_key):
    if(os.getenv("OPENAI_API_KEY")==None):
        openai.api_key = api_key

    if(not is_api_key_valid()):
       return "Not a valid key"
    
    if(type == "text"):
        prompt = user_in

    elif(type == "youtube"):
        transcript = YouTubeTranscriptApi.get_transcript(user_in)
        formatter = TextFormatter()
        prompt = "Summarize this video transcript in 200 words" + formatter.format_transcript(transcript)[0:3500]
        


    response = openai.Completion.create(
        model="text-davinci-003",
        prompt = prompt,
        temperature=0.6,
        max_tokens=200,
    )

    return(response.choices[0].text)
