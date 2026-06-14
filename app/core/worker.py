from PySide6.QtCore import QThread, Signal
import os
from app.core.downloader import download


class DownloadWorker(QThread):
    progress = Signal(int)
    status = Signal(str)

    def __init__(self, url: str, path: str, fmt: str, quality: str):
        super().__init__()
        self.url: str = url
        self.path: str = path
        self.fmt: str = fmt
        self.quality: str = quality
        self.save_path: str = ""  # Will be set during download

    def run(self) -> None:
        # Override the download function to capture the save path
        def progress_hook(value):
            self.progress.emit(value)
            
        def status_hook(msg):
            self.status.emit(msg)
            # Extract save path from status message if it contains "Saved to:"
            if "Saved to:" in msg:
                self.save_path = msg.split("Saved to:")[1].strip()
        
        download(
            self.url,
            self.path,
            self.fmt,
            self.quality,
            progress_hook,
            status_hook
        )