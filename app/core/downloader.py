import yt_dlp
import time
import random
import shutil
import os


def get_ffmpeg():
    return shutil.which("ffmpeg")


# =========================
# 🔥 REAL PROGRESS HOOK
# =========================
def make_hook(progress_cb, status_cb):
    def hook(d):
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            downloaded = d.get("downloaded_bytes", 0)

            if total:
                percent = int(downloaded / total * 100)
                progress_cb.emit(percent)

            speed = d.get("speed")
            eta = d.get("eta")

            if speed:
                speed_mb = speed / 1024 / 1024
                status_cb.emit(f"⬇ {round(speed_mb,2)} MB/s")

            if eta:
                status_cb.emit(f"⏳ ETA: {eta}s")

        elif d["status"] == "finished":
            progress_cb.emit(100)
            status_cb.emit("🔄 Processing...")

    return hook


# =========================
# BASE OPTIONS
# =========================
def base_opts(path, hook):
    return {
        "outtmpl": os.path.join(path, "%(title)s.%(ext)s"),
        "progress_hooks": [hook],

        "http_headers": {
            "User-Agent": "Mozilla/5.0"
        },

        "extractor_args": {
            "youtube": {
                "player_client": ["android", "web"]
            }
        },

        "quiet": True,
        "retries": 10,
        "fragment_retries": 10,
    }


# =========================
# VIDEO
# =========================
def mp4_opts(opts, quality):
    ffmpeg = get_ffmpeg()

    if quality == "Auto (Best)":
        if ffmpeg:
            opts["ffmpeg_location"] = ffmpeg
            opts["format"] = "bestvideo+bestaudio/best"
        else:
            opts["format"] = "best"
        return opts

    height = quality.replace("p", "")

    if ffmpeg:
        opts["ffmpeg_location"] = ffmpeg
        opts["format"] = f"bestvideo[height<={height}]+bestaudio/best"
    else:
        opts["format"] = f"best[height<={height}]/best"

    return opts


# =========================
# AUDIO
# =========================
def mp3_opts(opts, quality):
    bitrate = quality.replace(" kbps", "")

    opts.update({
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": bitrate,
        }],
    })

    return opts


# =========================
# MAIN DOWNLOAD
# =========================
def download(url, path, fmt, quality, progress, status):
    if not url.startswith("http"):
        status.emit("❌ Invalid URL")
        return

    os.makedirs(path, exist_ok=True)

    hook = make_hook(progress, status)

    time.sleep(random.uniform(1, 2))

    opts = base_opts(path, hook)

    try:
        if fmt == "MP4":
            opts = mp4_opts(opts, quality)
        else:
            opts = mp3_opts(opts, quality)

        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])

        status.emit("✅ Done!")

    except Exception as e:
        status.emit(f"❌ Error: {str(e)[:120]}")