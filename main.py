import os
import sys
from typing import Optional

from PySide6.QtWidgets import QApplication

from app.ui.login_window import LoginWindow
from app.ui.main_window import MainWindow
from app.utils.logger import get_logger
from config import settings


def _restore_session() -> bool:
    """Try to restore a saved session. Returns True on success."""
    if not os.path.exists(settings.session_file):
        return False
    try:
        with open(settings.session_file, "r", encoding="utf-8") as f:
            email = f.read().strip()
        if not email:
            return False
        from app.services.auth import auth_service
        auth_service.restore_session(email)
        return True
    except Exception:
        return False


def main() -> None:
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

    # Validate session before skipping login
    # TODO: store expiry / refresh_token in session file for real validation
    if _restore_session():
        log.info("Session restored, opening main window")
        open_main()
    else:
        log.info("No valid session, showing login window")
        if os.path.exists(settings.session_file):
            os.remove(settings.session_file)
        login_window = LoginWindow(open_main)
        login_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()