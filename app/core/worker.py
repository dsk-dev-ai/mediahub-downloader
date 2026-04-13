from PySide6.QtCore import QThread, Signal
from app.core.downloader import download


class DownloadWorker(QThread):
    progress = Signal(int)
    status = Signal(str)

    def __init__(self, url, path, fmt, quality):
        super().__init__()
        self.url = url
        self.path = path
        self.fmt = fmt
        self.quality = quality

    def run(self):
        download(
            self.url,
            self.path,
            self.fmt,
            self.quality,
            self.progress,
            self.status
        )
