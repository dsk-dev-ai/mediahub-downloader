import yt_dlp
import os
import shutil
from typing import Optional
from app.services.history import history_service


def get_ffmpeg() -> Optional[str]:
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
        opts["format"] = (
            f"bestvideo[height<={height}]+bestaudio/best"
            if ffmpeg else f"best[height<={height}]/best"
        )

    if ffmpeg:
        opts["ffmpeg_location"] = ffmpeg

    return opts


# ✅ FIXED: MP3 QUALITY SUPPORT
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


def download(url: str, path: str, fmt: str, quality: str, progress, status) -> None:
    try:
        if not url.startswith("http"):
            status.emit("❌ Invalid URL")
            return

        os.makedirs(path, exist_ok=True)

        hook = make_hook(progress, status)
        opts = base_opts(path, hook)

        if fmt == "MP4":
            opts = mp4_opts(opts, quality)
        else:
            opts = mp3_opts(opts, quality)  # ✅ FIXED CALL

        with yt_dlp.YoutubeDL(opts) as ydl:
            # Extract info first to get title
            info = ydl.extract_info(url, download=False)
            title = info.get("title", "Unknown Title")
            
            # Then download
            ydl.download([url])
            
            # Get the actual filename that was downloaded
            info = ydl.extract_info(url, download=False)
            filename = ydl.prepare_filename(info)
            
            # Adjust filename for MP3 (yt_dlp changes extension after postprocessing)
            if fmt == "MP3":
                filename = os.path.splitext(filename)[0] + ".mp3"
            
            # Add to history after successful download
            history_service.add_download(
                url=url,
                title=title,
                file_path=filename,
                format_type=fmt,
                quality=quality
            )

        status.emit("✅ Done!")

    except Exception as e:
        status.emit(f"❌ {str(e)}")