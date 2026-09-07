"""Automatic update service for MediaHub Downloader.
Checks for new versions and handles updates.
"""
import json
import threading
import urllib.request
from typing import Optional, Tuple

APP_VERSION = "1.0.0"
GITHUB_REPO = "your-username/mediahub-downloader"


class UpdateService:
    def __init__(self, current_version: str = APP_VERSION):
        self.current_version = current_version
        self.update_url = (
            f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
        )

    def check_for_updates(self) -> Tuple[bool, Optional[str], Optional[str]]:
        """Check if a new version is available.

        Returns:
            Tuple of (update_available, latest_version, release_notes)
        """
        try:
            req = urllib.request.Request(
                self.update_url,
                headers={"Accept": "application/vnd.github.v3+json"},
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())

            latest_version = data["tag_name"].lstrip("v")
            release_notes = data.get("body", "")

            update_available = self._is_version_newer(
                latest_version, self.current_version
            )
            return update_available, latest_version, release_notes

        except Exception:
            return False, None, None

    def start_background_update_check(self) -> None:
        """Spawn a daemon thread that checks for updates."""

        def _check():
            update_available, latest_version, release_notes = (
                self.check_for_updates()
            )
            if update_available:
                print(f"Update available: {latest_version}")
                if release_notes:
                    print(f"Release notes: {release_notes}")

        thread = threading.Thread(target=_check, daemon=True)
        thread.start()

    @staticmethod
    def _is_version_newer(latest: str, current: str) -> bool:
        """Simple dotted-version comparison."""
        try:
            latest_parts = [int(x) for x in latest.split(".")]
            current_parts = [int(x) for x in current.split(".")]
            return latest_parts > current_parts
        except (ValueError, AttributeError):
            return False


update_service = UpdateService()
