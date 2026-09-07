import os
import shutil


def get_ffmpeg():
    """Locate ffmpeg on the system PATH."""
    found = shutil.which("ffmpeg")
    if found:
        return found
    return None
