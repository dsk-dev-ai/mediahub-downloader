import os
import webbrowser

import qtawesome as qta
import requests
import yt_dlp
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QStackedWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.core.worker import DownloadWorker
from app.services.auth import auth_service
from app.services.payment import payment_service
from app.services.user import current_user


def icon(name):
    return qta.icon(f"fa5s.{name}", color="#22c55e")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MediaHub Pro")
        self.resize(1300, 780)
        self.worker = None

        self.preview_timer = QTimer()
        self.preview_timer.setSingleShot(True)
        self.preview_timer.timeout.connect(self.load_preview)

        self.build_ui()
        self.update_user()

    def apply_theme(self):
        self.setStyleSheet(
            """
        QWidget { background-color: #0b0f19; color: #e5e7eb; font-family: Segoe UI; }
        QLabel#title { font-size: 20px; font-weight: bold; }
        QLabel#sub { color: #9ca3af; }
        QFrame#card { background-color: #111827; border-radius: 12px; padding: 14px; border: 1px solid #1f2937; }
        QPushButton { padding: 10px; border-radius: 8px; background-color: #1f2937; }
        QPushButton#primary { background-color: #22c55e; font-weight: bold; color: #02140a; }
        QPushButton:hover { background-color: #374151; }
        QPushButton#primary:hover { background-color: #16a34a; }
        QLineEdit, QComboBox { padding: 10px; border-radius: 8px; background: #020617; border: 1px solid #1f2937; }
        QTextEdit { background-color: #020617; border-radius: 10px; }
        QProgressBar { background-color: #1f2937; border-radius: 8px; }
        QProgressBar::chunk { background-color: #22c55e; }
        """
        )

    def build_ui(self):
        self.apply_theme()
        root = QHBoxLayout(self)

        sidebar = QVBoxLayout()
        logo = QLabel("🎧 MediaHub")
        logo.setObjectName("title")

        self.btn_home = QPushButton("🏠 Home")
        self.btn_download = QPushButton("⬇ Downloader")
        self.btn_upgrade = QPushButton("🚀 Upgrade")

        sidebar.addWidget(logo)
        sidebar.addSpacing(20)
        sidebar.addWidget(self.btn_home)
        sidebar.addWidget(self.btn_download)
        sidebar.addWidget(self.btn_upgrade)
        sidebar.addStretch()
        root.addLayout(sidebar, 1)

        self.stack = QStackedWidget()
        root.addWidget(self.stack, 4)

        self.stack.addWidget(self.home_page())
        self.stack.addWidget(self.download_page())
        self.stack.addWidget(self.upgrade_page())

        self.btn_home.clicked.connect(lambda: self.switch(0))
        self.btn_download.clicked.connect(lambda: self.switch(1))
        self.btn_upgrade.clicked.connect(lambda: self.switch(2))

    def switch(self, index):
        self.stack.setCurrentIndex(index)

    def home_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)

        title = QLabel("👋 Welcome back")
        title.setObjectName("title")

        self.user_label = QLabel("Not logged in")
        self.stats = QLabel("📊 Downloads: 0   •   ⚡ Speed: —   •   ⏳ ETA: —")

        card_layout.addWidget(title)
        card_layout.addWidget(self.user_label)
        card_layout.addWidget(self.stats)
        layout.addWidget(card)
        layout.addStretch()
        return page

    def update_user(self):
        user = auth_service.get_user()
        self.user_label.setText(user.email if user else "Not logged in")

    def download_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(15)

        preview = QFrame()
        preview.setObjectName("card")
        p = QHBoxLayout(preview)

        self.thumb = QLabel()
        self.thumb.setFixedSize(200, 110)
        self.video_title = QLabel("Paste a URL to preview video")
        self.video_title.setWordWrap(True)

        p.addWidget(self.thumb)
        p.addWidget(self.video_title)

        self.url = QLineEdit()
        self.url.setPlaceholderText("Paste YouTube URL here...")
        self.url.textChanged.connect(lambda: self.preview_timer.start(600))

        options = QHBoxLayout()
        self.format = QComboBox()
        self.format.addItems(["MP4", "MP3"])
        self.format.currentTextChanged.connect(self.update_quality)

        self.quality = QComboBox()
        self.update_quality("MP4")

        options.addWidget(self.format)
        options.addWidget(self.quality)

        # ✅ FIXED DOWNLOAD PATH (ONLY CHANGE)
        path_row = QHBoxLayout()
        default_download_path = os.path.join(os.path.expanduser("~"), "Downloads", "MediaHub")
        os.makedirs(default_download_path, exist_ok=True)
        self.path = QLineEdit(default_download_path)

        browse = QPushButton("📂")
        browse.clicked.connect(self.pick_folder)

        path_row.addWidget(self.path)
        path_row.addWidget(browse)

        self.download_btn = QPushButton("⬇ Download")
        self.download_btn.setObjectName("primary")
        self.download_btn.clicked.connect(self.start_download)

        self.progress = QProgressBar()
        self.status = QLabel("🟢 Ready")
        self.speed = QLabel("⚡ Speed: waiting...")
        self.eta = QLabel("⏳ ETA: calculating...")

        self.logs = QTextEdit()
        self.logs.setReadOnly(True)

        layout.addWidget(preview)
        layout.addWidget(self.url)
        layout.addLayout(options)
        layout.addLayout(path_row)
        layout.addWidget(self.download_btn)
        layout.addWidget(self.progress)
        layout.addWidget(self.status)
        layout.addWidget(self.speed)
        layout.addWidget(self.eta)
        layout.addWidget(self.logs)
        return page

    def update_quality(self, fmt):
        self.quality.clear()
        if fmt == "MP4":
            self.quality.addItems(["Auto (Best)", "1080p", "720p", "480p"])
        else:
            self.quality.addItems(["320 kbps", "256 kbps", "128 kbps"])

    def pick_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.path.setText(folder)

    def load_preview(self):
        url = self.url.text().strip()
        if not url.startswith("http"):
            return

        try:
            with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
                info = ydl.extract_info(url, download=False)

            self.video_title.setText(info.get("title", "Untitled"))
            thumbnail = info.get("thumbnail")
            if not thumbnail:
                return

            image_data = requests.get(thumbnail, timeout=10).content
            pix = QPixmap()
            pix.loadFromData(image_data)
            self.thumb.setPixmap(pix.scaled(200, 110))
        except Exception:
            self.video_title.setText("Invalid URL or unable to load preview")

    def start_download(self):
        url = self.url.text().strip()
        if not url.startswith("http"):
            self.logs.append("❌ Invalid URL")
            return

        self.logs.clear()
        self.progress.setValue(0)
        self.download_btn.setEnabled(False)
        self.status.setText("🚀 Starting download...")

        self.worker = DownloadWorker(
            url,
            self.path.text(),
            self.format.currentText(),
            self.quality.currentText(),
        )
        self.worker.progress.connect(self.progress.setValue)
        self.worker.status.connect(self.update_status)
        self.worker.finished.connect(self.download_done)
        self.worker.start()

    def update_status(self, msg):
        self.logs.append(msg)
        self.status.setText(msg)
        if "MB/s" in msg:
            self.speed.setText(f"⚡ {msg}")
        if "ETA" in msg:
            self.eta.setText(f"⏳ {msg}")

    def download_done(self):
        self.download_btn.setEnabled(True)
        if "❌" not in self.status.text():
            self.status.setText("✅ Download completed")

    def upgrade_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        card = QFrame()
        card.setObjectName("card")
        c = QVBoxLayout(card)

        title = QLabel("🚀 Upgrade to PRO")
        title.setObjectName("title")

        features = QLabel(
            "✔ 1080p downloads\n✔ Faster speed\n✔ MP3 320kbps\n✔ Unlimited downloads"
        )

        stripe_btn = QPushButton("Pay with Stripe")
        stripe_btn.setObjectName("primary")
        stripe_btn.clicked.connect(self.pay_with_stripe)

        razorpay_btn = QPushButton("Pay with Razorpay")
        razorpay_btn.clicked.connect(self.pay_with_razorpay)

        offline_btn = QPushButton("Unlock PRO (dev/test)")
        offline_btn.clicked.connect(self.unlock_pro)

        c.addWidget(title)
        c.addWidget(features)
        c.addWidget(stripe_btn)
        c.addWidget(razorpay_btn)
        c.addWidget(offline_btn)

        layout.addWidget(card)
        layout.addStretch()
        return page

    def pay_with_stripe(self):
        user = auth_service.get_user()
        email = user.email if user else "customer@example.com"
        ok, payload = payment_service.create_stripe_checkout(email)
        if ok:
            webbrowser.open(payload)
            QMessageBox.information(self, "Stripe", "Checkout opened in your browser.")
        else:
            QMessageBox.warning(self, "Stripe", payload)

    def pay_with_razorpay(self):
        ok, payload = payment_service.create_razorpay_order()
        if ok:
            QMessageBox.information(self, "Razorpay", payload)
        else:
            QMessageBox.warning(self, "Razorpay", payload)

    def unlock_pro(self):
        current_user.is_pro = True
        QMessageBox.information(self, "Success", "🎉 PRO unlocked!")
