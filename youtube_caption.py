import os
import json
import logging
import re
import subprocess
import tempfile
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from crewai.tools import tool

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def extract_video_id(url):
    import re
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    return match.group(1) if match else None

@tool("YouTube Caption Extractor")
def youtube_caption_tool(youtube_url: str) -> str:
    """
    Extracts transcript/captions from a YouTube video using its URL.
    Falls back to yt-dlp if direct extraction fails.
    """
    logger.info(f"Processing YouTube URL: {youtube_url}")
    video_id = extract_video_id(youtube_url)

    if not video_id:
        logger.error("Invalid YouTube URL or could not extract video ID.")
        return "Invalid YouTube URL."

    # Preferred: YouTubeTranscriptApi
    try:
        logger.info("Trying YouTubeTranscriptApi...")
        languages = ["en", "en-US", "en-GB", "hi", "hi-IN"]
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
        full_text = " ".join([entry["text"] for entry in transcript])
        logger.info("Transcript successfully extracted via YouTubeTranscriptApi")
        return full_text if full_text else "Transcript not available."
    except Exception as e:
        logger.error(f"YouTubeTranscriptApi failed. Trying yt-dlp fallback...")

    # yt-dlp fallback
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            cmd = [
                "yt-dlp",
                "--skip-download",
                "--write-auto-sub",
                "--sub-lang", "en",
                "--sub-format", "vtt",
                "-o", os.path.join(tmpdir, "%(id)s.%(ext)s"),
                youtube_url
            ]
            subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=30)

            vtt_file = os.path.join(tmpdir, f"{video_id}.en.vtt")
            if not os.path.exists(vtt_file):
                logger.error("yt-dlp did not generate subtitle file.")
                return "Transcript not available or yt-dlp did not generate subtitles."

            with open(vtt_file, "r", encoding="utf-8") as f:
                lines = f.readlines()

            transcript_lines = []
            for line in lines:
                line = line.strip()
                if (
                    line and
                    not line.startswith("WEBVTT") and
                    "-->" not in line and
                    not re.match(r"^\d+$", line)
                ):
                    transcript_lines.append(line)

            full_text = " ".join(transcript_lines).strip()
            logger.info("Transcript successfully extracted from .vtt via yt-dlp")
            return full_text if full_text else "Transcript not available or empty."

    except subprocess.TimeoutExpired:
        logger.error("yt-dlp process timed out")
        return "yt-dlp took too long and was forcefully stopped. Transcript not available."
    except Exception as e:
        logger.error(f"yt-dlp fallback failed: {e}")
        return "yt-dlp fallback failed. Transcript not available."
