import openai
import os
from dotenv import load_dotenv

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from youtube_transcript_api.formatters import JSONFormatter

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def text_request(user_in):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt = user_in,
        temperature=0.6,
        max_tokens=50,
    )

    return(response.choices[0].text)



# test video id: bBQVR4epfBQ&pp=ygUScGVydW4gcmVxdWlyZW1lbnRz

def youtube_request(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    formatter = TextFormatter()


    transcript_text = formatter.format_transcript(transcript)

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt = "Summarize this transcript" + transcript_text[0:3000],
        temperature=0.6,
        max_tokens=50,
    )

    return(response.choices[0].text)