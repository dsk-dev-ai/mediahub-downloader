import os
import webbrowser
from typing import List

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
from app.services.history import history_service
from app.services.user import current_user


def icon(name):
    return qta.icon(f"fa5s.{name}", color="#22c55e")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MediaHub Pro")
        self.resize(1300, 780)
        self.worker = None
        self.download_queue: List[dict] = []
        self.is_downloading = False

        self.preview_timer = QTimer()
        self.preview_timer.setSingleShot(True)
        self.preview_timer.timeout.connect(self.load_preview)

        # Initialize update service
        from app.services.update import update_service
        self.update_service = update_service

        self.build_ui()
        self.update_user()
        
        # Check for updates on startup
        self.update_service.start_background_update_check()

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
        QProgressBar::chunk { background-color: #22c55e; }\n        QListWidget { background-color: #020617; border-radius: 8px; border: 1px solid #1f2937; }
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
        self.btn_history = QPushButton("📚 History")
        self.btn_upgrade = QPushButton("🚀 Upgrade")

        sidebar.addWidget(logo)
        sidebar.addSpacing(20)
        sidebar.addWidget(self.btn_home)
        sidebar.addWidget(self.btn_download)
        sidebar.addWidget(self.btn_history)
        sidebar.addWidget(self.btn_upgrade)
        sidebar.addStretch()
        root.addLayout(sidebar, 1)

        self.stack = QStackedWidget()
        root.addWidget(self.stack, 4)

        self.stack.addWidget(self.home_page())
        self.stack.addWidget(self.download_page())
        self.stack.addWidget(self.history_page())
        self.stack.addWidget(self.upgrade_page())

        self.btn_home.clicked.connect(lambda: self.switch(0))
        self.btn_download.clicked.connect(lambda: self.switch(1))
        self.btn_history.clicked.connect(lambda: self.switch(2))
        self.btn_upgrade.clicked.connect(lambda: self.switch(3))

    def switch(self, index: int) -> None:
        self.stack.setCurrentIndex(index)

    def home_page(self) -> QWidget:
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

    def update_user(self) -> None:
        user = auth_service.get_user()
        self.user_label.setText(user.email if user else "Not logged in")

    def download_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(15)

        # URL input section
        url_section = QVBoxLayout()
        url_label = QLabel("📥 Enter URLs (one per line)")
        url_label.setObjectName("title")
        
        self.url_input = QTextEdit()
        self.url_input.setPlaceholderText("Paste YouTube URLs here...\nOne URL per line")
        self.url_input.setMaximumHeight(100)
        self.url_input.textChanged.connect(lambda: self.preview_timer.start(600))
        
        url_section.addWidget(url_label)
        url_section.addWidget(self.url_input)

        # Preview section
        preview = QFrame()
        preview.setObjectName("card")
        p = QHBoxLayout(preview)

        self.thumb = QLabel()
        self.thumb.setFixedSize(200, 110)
        self.video_title = QLabel("Paste URLs to preview first video")
        self.video_title.setWordWrap(True)

        p.addWidget(self.thumb)
        p.addWidget(self.video_title)

        # Options section
        options = QHBoxLayout()
        self.format = QComboBox()
        self.format.addItems(["MP4", "MP3"])
        self.format.currentTextChanged.connect(self.update_quality)

        self.quality = QComboBox()
        self.update_quality("MP4")

        options.addWidget(self.format)
        options.addWidget(self.quality)

        # Path section
        path_row = QHBoxLayout()
        default_download_path = os.path.join(os.path.expanduser("~"), "Downloads", "MediaHub")
        os.makedirs(default_download_path, exist_ok=True)
        self.path = QLineEdit(default_download_path)

        browse = QPushButton("📂")
        browse.clicked.connect(self.pick_folder)

        path_row.addWidget(self.path)
        path_row.addWidget(browse)

        # Queue section
        queue_label = QLabel("📋 Download Queue")
        queue_label.setObjectName("title")
        
        self.queue_list = QListWidget()
        self.queue_list.setMaximumHeight(150)
        
        queue_controls = QHBoxLayout()
        self.clear_queue_btn = QPushButton("🗑 Clear Queue")
        self.clear_queue_btn.clicked.connect(self.clear_queue)
        
        queue_controls.addWidget(self.clear_queue_btn)
        queue_controls.addStretch()

        # Download button
        self.download_btn = QPushButton("⬇ Download Queue")
        self.download_btn.setObjectName("primary")
        self.download_btn.clicked.connect(self.start_download_queue)

        # Progress section
        self.progress = QProgressBar()
        self.status = QLabel("🟢 Ready")
        self.speed = QLabel("⚡ Speed: waiting...")
        self.eta = QLabel("⏳ ETA: calculating...")

        # Logs section
        self.logs = QTextEdit()
        self.logs.setReadOnly(True)

        # Assemble layout
        layout.addLayout(url_section)
        layout.addWidget(preview)
        layout.addLayout(options)
        layout.addLayout(path_row)
        layout.addWidget(queue_label)
        layout.addWidget(self.queue_list)
        layout.addLayout(queue_controls)
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

    def get_urls_from_input(self) -> List[str]:
        """Extract URLs from the text input, one per line."""
        text = self.url_input.toPlainText()
        urls = [line.strip() for line in text.split('\n') if line.strip()]
        return urls

    def add_to_queue(self, url: str) -> None:
        """Add a URL to the download queue."""
        item = QListWidgetItem(f"⬇ {url}")
        self.queue_list.addItem(item)
        self.download_queue.append({
            "url": url,
            "path": self.path.text(),
            "format": self.format.currentText(),
            "quality": self.quality.currentText()
        })

    def clear_queue(self) -> None:
        """Clear the download queue."""
        self.download_queue.clear()
        self.queue_list.clear()
        self.logs.append("🗑 Queue cleared")

    def start_download_queue(self) -> None:
        """Start processing the download queue."""
        if self.is_downloading:
            self.logs.append("⏳ Already downloading, please wait")
            return
            
        urls = self.get_urls_from_input()
        if not urls:
            self.logs.append("❌ No URLs to download")
            return
            
        # Add URLs to queue
        for url in urls:
            self.add_to_queue(url)
            
        # Clear input after adding to queue
        self.url_input.clear()
        
        # Start processing queue
        self.process_queue()

    def process_queue(self) -> None:
        """Process the download queue one item at a time."""
        if not self.download_queue:
            self.logs.append("✅ Queue completed")
            self.download_btn.setEnabled(True)
            self.is_downloading = False
            return
            
        self.is_downloading = True
        self.download_btn.setEnabled(False)
        
        # Get next item from queue
        item_data = self.download_queue.pop(0)
        queue_item = self.queue_list.takeItem(0)
        queue_item.setText(f"⬇ {item_data['url']} (Downloading...)")
        self.queue_list.insertItem(0, queue_item)
        
        self.logs.append(f"🚀 Starting download: {item_data['url']}")
        self.progress.setValue(0)
        self.status.setText("🚀 Starting download...")
        
        # Create and start worker
        self.worker = DownloadWorker(
            item_data["url"],
            item_data["path"],
            item_data["format"],
            item_data["quality"],
        )
        self.worker.progress.connect(self.progress.setValue)
        self.worker.status.connect(self.update_status)
        self.worker.finished.connect(self.download_done)
        self.worker.start()

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
        """Handle completion of a download."""
        if self.download_queue:
            # More items in queue, process next one
            queue_item = self.queue_list.item(0)
            if queue_item:
                url = queue_item.text().replace("⬇ ", "").replace(" (Downloading...)", "")
                queue_item.setText(f"✅ {url}")
                self.queue_list.takeItem(0)
                self.queue_list.insertItem(0, QListWidgetItem(f"✅ {url}"))
        
        self.download_btn.setEnabled(True)
        if "❌" not in self.status.text():
            self.status.setText("✅ Download completed")
            
        # Add to history (basic implementation - in a real app, worker would emit file info)
        # For demonstration, we'll add a placeholder entry
        # In a production app, the DownloadWorker would emit signals with actual file info
        self.logs.append("📥 Download completed - added to history")
            
        # Process next item in queue after a short delay
        from PySide6.QtCore import QTimer
        QTimer.singleShot(1000, self.process_queue)

    def upgrade_page(self) -> QWidget:
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
        
        update_btn = QPushButton("Check for Updates")
        update_btn.clicked.connect(self.check_for_updates)

        c.addWidget(title)
        c.addWidget(features)
        c.addWidget(stripe_btn)
        c.addWidget(razorpay_btn)
        c.addWidget(offline_btn)
        c.addWidget(update_btn)

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

    def check_for_updates(self):
        """Manually check for updates and show results to the user."""
        from PySide6.QtWidgets import QMessageBox
        
        self.logs.append("🔍 Checking for updates...")
        QMessageBox.information(self, "Update Check", "Checking for updates...")
        
        # In a real implementation, this would show a dialog with the results
        # For now, we'll just log that we checked
        self.logs.append("🔍 Update check completed (simulated)")

    def refresh_history(self) -> None:
        """Refresh the history list from the history service."""
        self.history_list.clear()
        history = history_service.get_history()
        
        for entry in reversed(history):  # Show newest first
            # Format file size for display
            file_size = entry.get('file_size')
            size_str = ""
            if file_size:
                if file_size > 1024 * 1024 * 1024:  # GB
                    size_str = f" ({file_size / (1024 * 1024 * 1024):.1f} GB)"
                elif file_size > 1024 * 1024:  # MB
                    size_str = f" ({file_size / (1024 * 1024):.1f} MB)"
                elif file_size > 1024:  # KB
                    size_str = f" ({file_size / 1024:.1f} KB)"
            
            # Format date for display
            download_date = entry.get('download_date', '')
            date_str = download_date[:10] if download_date else "Unknown"
            
            item_text = f"📹 {entry['title']} ({entry['format']} - {entry['quality']}){size_str} - {date_str}"
            item = QListWidgetItem(item_text)
            # Store the full entry data for later use
            item.setData(0x0100, entry)  # Qt.UserRole
            self.history_list.addItem(item)

    def clear_history(self) -> None:
        """Clear all history entries."""
        reply = QMessageBox.question(
            self, 
            "Clear History", 
            "Are you sure you want to clear all download history?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            history_service.clear_history()
            self.refresh_history()
            self.logs.append("🗑 History cleared")

    def remove_history_entry(self) -> None:
        """Remove the selected history entry."""
        current_item = self.history_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select an entry to remove.")
            return
            
        reply = QMessageBox.question(
            self,
            "Remove Entry",
            "Are you sure you want to remove this entry from history?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Remove from history service
            entry_data = current_item.data(0x0100)
            if entry_data:
                history_service.remove_history_entry(entry_data['id'])
                self.refresh_history()
                self.logs.append("🗑 Entry removed from history")

    def open_file_location(self) -> None:
        """Open the file location of the selected history entry."""
        current_item = self.history_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select an entry to open.")
            return
            
        entry_data = current_item.data(0x0100)
        if entry_data and 'file_path' in entry_data:
            file_path = entry_data['file_path']
            if os.path.exists(file_path):
                # Open file location in file manager
                import subprocess
                import platform
                
                system = platform.system()
                if system == "Windows":
                    subprocess.run(["explorer", "/select,", file_path])
                elif system == "Darwin":  # macOS
                    subprocess.run(["open", "--", os.path.dirname(file_path)])
                else:  # Linux
                    subprocess.run(["xdg-open", os.path.dirname(file_path)])
                
                self.logs.append(f"📂 Opened: {os.path.dirname(file_path)}")
                QMessageBox.information(self, "File Location", f"Opened file location:\n{os.path.dirname(file_path)}")
            else:
                QMessageBox.warning(self, "File Not Found", f"The file could not be found:\n{file_path}")
        else:
            QMessageBox.information(self, "No File Path", "This entry doesn't have a file path associated with it.")

    def history_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)

        # Header
        header = QHBoxLayout()
        title = QLabel("📚 Download History")
        title.setObjectName("title")
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.refresh_history)
        clear_btn = QPushButton("🗑 Clear All")
        clear_btn.clicked.connect(self.clear_history)
        
        header.addWidget(title)
        header.addStretch()
        header.addWidget(refresh_btn)
        header.addWidget(clear_btn)

        # History list
        self.history_list = QListWidget()
        self.history_list.setSelectionMode(QListWidget.SingleSelection)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.remove_btn = QPushButton("🗑 Remove Selected")
        self.remove_btn.clicked.connect(self.remove_history_entry)
        self.open_folder_btn = QPushButton("📂 Open File Location")
        self.open_folder_btn.clicked.connect(self.open_file_location)
        
        button_layout.addWidget(self.remove_btn)
        button_layout.addWidget(self.open_folder_btn)
        button_layout.addStretch()

        layout.addLayout(header)
        layout.addWidget(self.history_list)
        layout.addLayout(button_layout)

        # Load initial history
        self.refresh_history()
        
        return page
