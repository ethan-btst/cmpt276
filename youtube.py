from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from youtube_transcript_api.formatters import JSONFormatter

# bBQVR4epfBQ&pp=ygUScGVydW4gcmVxdWlyZW1lbnRz

def youtube_request(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    formatter = TextFormatter()


    transcript_text = formatter.format_transcript(transcript)

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt = "Summarize this transcript" + transcript_text,
        temperature=0.6,
        max_tokens=50,
    )

    return(response.choices[0].text)