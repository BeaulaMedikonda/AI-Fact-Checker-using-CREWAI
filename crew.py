from crewai.tools import tool
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import re

def extract_video_id(url: str) -> str:
    # Handles different YouTube URL formats
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    return match.group(1) if match else None

@tool("youtube_caption_tool")
def youtube_caption_tool(input_youtube_url: str) -> str:
    """Extract transcript from a YouTube video URL for fact-checking its content."""
    try:
        video_id = extract_video_id(input_youtube_url)
        if not video_id:
            return "Invalid YouTube URL format. Please provide a valid one."

        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_transcript = " ".join([t["text"] for t in transcript])
        return f"Transcript extracted successfully. Content: {full_transcript[:2000]}..."  # Limit to first 2000 characters
    except TranscriptsDisabled:
        return "Transcript is disabled for this video."
    except NoTranscriptFound:
        return "No transcript found for this video."
    except Exception as e:
        return f"Error fetching transcript: {str(e)}"
