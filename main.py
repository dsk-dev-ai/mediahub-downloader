import os
import sys

from PySide6.QtWidgets import QApplication

from app.ui.login_window import LoginWindow
from app.ui.main_window import MainWindow
from config import settings


def main():
    app = QApplication(sys.argv)

    login_window = None
    main_window = None

    def open_main():
        nonlocal main_window, login_window
        if login_window:
            login_window.close()

        main_window = MainWindow()
        main_window.show()
        main_window.activateWindow()
        main_window.raise_()

    if os.path.exists(settings.session_file):
        open_main()
    else:
        login_window = LoginWindow(open_main)
        login_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
