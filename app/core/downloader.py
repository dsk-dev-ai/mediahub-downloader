import yt_dlp
import os
import shutil


def get_ffmpeg():
    return shutil.which("ffmpeg")


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


def base_opts(path, hook):
    return {
        "outtmpl": os.path.join(path, "%(title)s.%(ext)s"),
        "progress_hooks": [hook],
        "quiet": True,
        "retries": 10,
    }


def mp4_opts(opts, quality):
    ffmpeg = get_ffmpeg()

    if quality == "Auto (Best)":
        opts["format"] = "bestvideo+bestaudio/best" if ffmpeg else "best"
    else:
        height = quality.replace("p", "")
        opts["format"] = f"bestvideo[height<={height}]+bestaudio/best"

    if ffmpeg:
        opts["ffmpeg_location"] = ffmpeg

    return opts


def mp3_opts(opts):
    opts.update({
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
        }],
    })
    return opts


def download(url, path, fmt, quality, progress, status):
    try:
        os.makedirs(path, exist_ok=True)

        hook = make_hook(progress, status)
        opts = base_opts(path, hook)

        if fmt == "MP4":
            opts = mp4_opts(opts, quality)
        else:
            opts = mp3_opts(opts)

        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])

        status.emit("✅ Done!")

    except Exception as e:
        status.emit(f"❌ {str(e)}")
