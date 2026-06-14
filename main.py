import os
import sys
from typing import Optional

from PySide6.QtWidgets import QApplication

from app.ui.login_window import LoginWindow
from app.ui.main_window import MainWindow
from app.utils.logger import get_logger
from config import settings


def main() -> None:
    # Initialize logging
    log = get_logger("main")
    log.info("Starting MediaHub Downloader")
    
    app = QApplication(sys.argv)

    login_window: Optional[LoginWindow] = None
    main_window: Optional[MainWindow] = None

    def open_main() -> None:
        nonlocal main_window, login_window
        if login_window:
            login_window.close()
            log.info("Closed login window")

        main_window = MainWindow()
        main_window.show()
        main_window.activateWindow()
        main_window.raise_()
        log.info("Opened main window")

    if os.path.exists(settings.session_file):
        log.info("Session found, opening main window")
        open_main()
    else:
        log.info("No session found, showing login window")
        login_window = LoginWindow(open_main)
        login_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()