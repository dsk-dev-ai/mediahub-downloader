import sys
import os
from PySide6.QtWidgets import QApplication

from app.ui.login_window import LoginWindow
from app.ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    login_window = None
    main_window = None

    # =========================
    # OPEN DASHBOARD (FIXED)
    # =========================
    def open_main():
        nonlocal main_window, login_window

        # CLOSE LOGIN FIRST
        if login_window:
            login_window.close()

        # CREATE NEW MAIN WINDOW (IMPORTANT)
        main_window = MainWindow()
        main_window.show()
        main_window.activateWindow()
        main_window.raise_()

    # =========================
    # AUTO LOGIN
    # =========================
    if os.path.exists("session.txt"):
        open_main()
    else:
        login_window = LoginWindow(open_main)
        login_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()