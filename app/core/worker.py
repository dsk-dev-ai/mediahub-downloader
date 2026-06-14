from PySide6.QtCore import QThread, Signal
from app.core.downloader import download_media


class DownloadWorker(QThread):
    progress = Signal(int)
    status = Signal(str)
    finished = Signal()

    def __init__(self, url, path, format_choice, quality):
        super().__init__()
        self.url = url
        self.path = path
        self.format = format_choice
        self.quality = quality

    def run(self):
        def progress_hook(d):
            if d['status'] == 'downloading':
                # Calculate percentage
                if d.get('total_bytes') and d.get('downloaded_bytes'):
                    percent = int(d['downloaded_bytes'] / d['total_bytes'] * 100)
                    self.progress.emit(percent)
                elif d.get('total_bytes_estimate') and d.get('downloaded_bytes'):
                    percent = int(d['downloaded_bytes'] / d['total_bytes_estimate'] * 100)
                    self.progress.emit(percent)

                # Emit speed and ETA info
                if d.get('speed'):
                    speed_mb = d['speed'] / 1024 / 1024  # Convert to MB/s
                    self.status.emit(f"⬇ {speed_mb:.1f} MB/s")
                if d.get('eta'):
                    from datetime import timedelta
                    eta = str(timedelta(seconds=d['eta']))
                    self.status.emit(f"⏳ ETA: {eta}")

            elif d['status'] == 'finished':
                self.status.emit("✅ Processing...")

        success = download_media(
            self.url,
            self.path,
            self.format,
            self.quality,
            progress_hook
        )

        if success:
            self.status.emit("✅ Download completed")
        else:
            self.status.emit("❌ Download failed")

        self.finished.emit()