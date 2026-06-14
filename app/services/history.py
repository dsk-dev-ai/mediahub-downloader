"""
Download history service for MediaHub Downloader.
Tracks downloaded files and provides library management features.
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class HistoryService:
    def __init__(self, history_file: str = "download_history.json"):
        self.history_file = Path.home() / ".mediahub" / history_file
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        self.history: List[Dict] = self._load_history()

    def _load_history(self) -> List[Dict]:
        """Load download history from file."""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def _save_history(self) -> None:
        """Save download history to file."""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, default=str)
        except Exception:
            pass  # Fail silently to not disrupt user experience

    def add_download(self, url: str, title: str, file_path: str, 
                    format_type: str, quality: str) -> None:
        """Add a download to the history."""
        entry = {
            "url": url,
            "title": title,
            "file_path": file_path,
            "format": format_type,
            "quality": quality,
            "download_date": datetime.now().isoformat(),
            "file_size": self._get_file_size(file_path)
        }
        
        # Remove duplicates (same URL and title)
        self.history = [
            entry for entry in self.history 
            if not (entry.get("url") == url and entry.get("title") == title)
        ]
        
        # Add new entry at the beginning
        self.history.insert(0, entry)
        
        # Keep only last 100 entries
        self.history = self.history[:100]
        
        self._save_history()

    def _get_file_size(self, file_path: str) -> Optional[int]:
        """Get file size in bytes, or None if file doesn't exist."""
        try:
            return os.path.getsize(file_path) if os.path.exists(file_path) else None
        except Exception:
            return None

    def get_history(self) -> List[Dict]:
        """Get all download history entries."""
        return self.history.copy()

    def clear_history(self) -> None:
        """Clear all download history."""
        self.history.clear()
        self._save_history()

    def remove_entry(self, index: int) -> bool:
        """Remove a history entry by index."""
        if 0 <= index < len(self.history):
            self.history.pop(index)
            self._save_history()
            return True
        return False

    def search_history(self, query: str) -> List[Dict]:
        """Search history by URL or title."""
        query = query.lower()
        return [
            entry for entry in self.history
            if query in entry.get("url", "").lower() or 
               query in entry.get("title", "").lower()
        ]


# Global history service instance
history_service = HistoryService()