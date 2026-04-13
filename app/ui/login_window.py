from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QTimer
from app.services.auth import auth_service
from config import settings


class LoginWindow(QWidget):
    def __init__(self, open_main_callback):
        super().__init__()

        self.open_main = open_main_callback
        self.cooldown = False

        self.setWindowTitle("MediaHub Login")
        self.resize(380, 320)

        # ========================
        # 🎨 MODERN STYLE
        # ========================
        self.setStyleSheet("""
            QWidget {
                background-color: #0b0f19;
                color: #e5e7eb;
                font-family: Segoe UI;
            }

            QLineEdit {
                padding: 10px;
                border-radius: 8px;
                background: #111827;
                border: 1px solid #1f2937;
            }

            QPushButton {
                padding: 10px;
                border-radius: 8px;
                background-color: #22c55e;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #16a34a;
            }

            QPushButton:disabled {
                background-color: #374151;
            }

            QLabel#status {
                font-size: 13px;
            }
        """)

        # ========================
        # 📦 MAIN LAYOUT (CENTERED CARD)
        # ========================
        outer = QVBoxLayout(self)
        outer.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setFixedWidth(320)
        card.setStyleSheet("""
            QFrame {
                background-color: #111827;
                border-radius: 12px;
                padding: 20px;
                border: 1px solid #1f2937;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setSpacing(12)

        # ========================
        # 🎧 TITLE
        # ========================
        title = QLabel("🎧 MediaHub")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")

        # ========================
        # INPUTS
        # ========================
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        # ENTER KEY LOGIN
        self.password_input.returnPressed.connect(self.handle_login)

        self.remember = QCheckBox("🔐 Remember me")

        # ========================
        # STATUS
        # ========================
        self.label = QLabel("")
        self.label.setObjectName("status")
        self.label.setAlignment(Qt.AlignCenter)

        # ========================
        # BUTTONS
        # ========================
        self.btn_login = QPushButton("Login")
        self.btn_signup = QPushButton("Create Account")

        self.btn_login.clicked.connect(self.handle_login)
        self.btn_signup.clicked.connect(self.handle_signup)

        # ========================
        # BUILD UI
        # ========================
        layout.addWidget(title)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.remember)
        layout.addWidget(self.btn_login)
        layout.addWidget(self.btn_signup)
        layout.addWidget(self.label)

        outer.addWidget(card)

    # ========================
    # 🔁 RESET STATE
    # ========================
    def reset_buttons(self):
        self.cooldown = False
        self.btn_login.setEnabled(True)
        self.btn_signup.setEnabled(True)
        self.btn_login.setText("Login")

    # ========================
    # 🔐 LOGIN
    # ========================
    def handle_login(self):
        if self.cooldown:
            self.label.setText("⏳ Please wait...")
            return

        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not email or not password:
            self.label.setText("❌ Enter email & password")
            self.label.setStyleSheet("color: red;")
            return

        self.cooldown = True
        self.btn_login.setEnabled(False)
        self.btn_login.setText("Logging in...")

        success, msg = auth_service.login(email, password)

        self.label.setText(msg)

        if success:
            self.label.setStyleSheet("color: #22c55e;")

            # 🔐 SAVE SESSION
            if self.remember.isChecked():
                with open(settings.session_file, "w", encoding="utf-8") as f:
                    f.write(email)

            QTimer.singleShot(500, self.finish_login)
            return

        # ❌ error
        self.label.setStyleSheet("color: red;")
        QTimer.singleShot(3000, self.reset_buttons)

    def finish_login(self):
        self.open_main()
        self.close()

    # ========================
    # 📝 SIGNUP
    # ========================
    def handle_signup(self):
        if self.cooldown:
            self.label.setText("⏳ Please wait...")
            return

        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not email or not password:
            self.label.setText("❌ Enter email & password")
            self.label.setStyleSheet("color: red;")
            return

        self.cooldown = True
        self.btn_signup.setEnabled(False)

        success, msg = auth_service.signup(email, password)
        self.label.setText(msg)

        if success:
            self.label.setStyleSheet("color: #22c55e;")
        else:
            self.label.setStyleSheet("color: red;")

        QTimer.singleShot(3000, self.reset_buttons)