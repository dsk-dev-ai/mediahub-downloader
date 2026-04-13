import yt_dlp
import os
import shutil


def get_ffmpeg():
    return shutil.which("ffmpeg")


# =========================
# 🔥 CLEAN PROGRESS HOOK
# =========================
def make_hook(progress_signal, status_signal):
    def hook(data):
        state = data.get("status")

        if state == "downloading":
            total = data.get("total_bytes") or data.get("total_bytes_estimate")
            downloaded = data.get("downloaded_bytes", 0)

            if total:
                percent = int(downloaded / total * 100)
                progress_signal.emit(percent)

            speed = data.get("speed")
            eta = data.get("eta")

            if speed:
                status_signal.emit(f"⬇ {speed/1024/1024:.2f} MB/s")

            if eta:
                status_signal.emit(f"⏳ ETA: {eta}s")

        elif state == "finished":
            progress_signal.emit(100)
            status_signal.emit("🔄 Processing...")

    return hook


# =========================
# BASE OPTIONS
# =========================
def base_opts(path, hook):
    return {
        "outtmpl": os.path.join(path, "%(title)s.%(ext)s"),
        "progress_hooks": [hook],
        "http_headers": {"User-Agent": "Mozilla/5.0"},
        "extractor_args": {"youtube": {"player_client": ["android", "web"]}},
        "quiet": True,
        "retries": 10,
        "fragment_retries": 10,
    }


# =========================
# VIDEO OPTIONS
# =========================
def mp4_opts(opts, quality):
    ffmpeg = get_ffmpeg()

    if quality == "Auto (Best)":
        opts["format"] = "bestvideo+bestaudio/best" if ffmpeg else "best"
    else:
        height = quality.replace("p", "")
        opts["format"] = (
            f"bestvideo[height<={height}]+bestaudio/best"
            if ffmpeg else f"best[height<={height}]/best"
        )

    if ffmpeg:
        opts["ffmpeg_location"] = ffmpeg

    return opts


# =========================
# AUDIO OPTIONS
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
        status.emit(f"❌ Error: {str(e)[:150]}")
