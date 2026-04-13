import os

def get_ffmpeg():
    base = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    return os.path.join(base, "assets", "ffmpeg", "ffmpeg.exe")