import os
import yt_dlp
from typing import Optional


def download_media(
    url: str,
    output_path: str,
    format_choice: str,
    quality: str,
    progress_hook=None,
) -> bool:
    """
    Download media from URL with specified format and quality.

    Args:
        url: Video URL to download
        output_path: Directory to save the file
        format_choice: Either 'MP4' or 'MP3'
        quality: Quality setting (e.g., '1080p', '320 kbps')
        progress_hook: Optional callback for download progress

    Returns:
        True if download successful, False otherwise
    """
    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)

    # Configure yt-dlp options based on format and quality
    ydl_opts = {
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook] if progress_hook else [],
    }

    if format_choice == 'MP4':
        # Video format selection
        if quality == 'Auto (Best)':
            ydl_opts['format'] = 'bestvideo+bestaudio/best'
        elif quality == '1080p':
            ydl_opts['format'] = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
        elif quality == '720p':
            ydl_opts['format'] = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
        elif quality == '480p':
            ydl_opts['format'] = 'bestvideo[height<=480]+bestaudio/best[height<=480]'
        else:
            ydl_opts['format'] = 'bestvideo+bestaudio/best'
            
        # Merge video and audio
        ydl_opts['merge_output_format'] = 'mp4'

    elif format_choice == 'MP3':
        # Audio format selection
        if quality == '320 kbps':
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }]
        elif quality == '256 kbps':
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '256',
            }]
        elif quality == '128 kbps':
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',
            }]
        else:
            # Default to best audio quality
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return True
    except Exception as e:
        print(f"Download error: {e}")
        return False