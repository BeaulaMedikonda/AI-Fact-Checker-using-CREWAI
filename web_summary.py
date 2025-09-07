from youtube_transcript_api import YouTubeTranscriptApi
from crewai.tools import tool

@tool("Extract transcript from YouTube video")
def youtube_caption_tool(input_youtube_url: str) -> str:
    """Takes a YouTube URL and returns the full transcript text"""
    try:
        # Extract video ID robustly
        video_id = input_youtube_url.split("v=")[-1].split("&")[0].split("?si")[0]
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([entry["text"] for entry in transcript_list])
        return transcript
    except Exception as e:
        return f"Transcript could not be extracted: {str(e)}"
