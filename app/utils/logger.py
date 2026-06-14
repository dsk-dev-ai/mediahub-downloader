"""Structured logging system for MediaHub Downloader."""
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


class MediaHubLogger:
    """Custom logger for MediaHub Downloader with structured logging."""
    
    _instance: Optional['MediaHubLogger'] = None
    _logger: Optional[logging.Logger] = None
    
    def __new__(cls) -> 'MediaHubLogger':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._logger is None:
            self._setup_logger()
    
    def _setup_logger(self):
        """Set up the logger with appropriate handlers and formatters."""
        self._logger = logging.getLogger("mediahub")
        self._logger.setLevel(logging.DEBUG)
        
        # Prevent duplicate handlers
        if self._logger.handlers:
            return
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(funcName)s() | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        simple_formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%H:%M:%S'
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)
        self._logger.addHandler(console_handler)
        
        # File handler (rotating)
        try:
            log_dir = Path.home() / ".mediahub" / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)
            
            log_file = log_dir / f"mediahub_{datetime.now().strftime('%Y%m%d')}.log"
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(detailed_formatter)
            self._logger.addHandler(file_handler)
        except Exception:
            # If we can't create log file, continue with console only
            pass
    
    def get_logger(self, name: str = None) -> logging.Logger:
        """Get a logger instance."""
        if name:
            return self._logger.getChild(name)
        return self._logger
    
    def set_level(self, level: int):
        """Set the logging level."""
        self._logger.setLevel(level)
        for handler in self._logger.handlers:
            handler.setLevel(level)


# Global logger instance
logger = MediaHubLogger()


def get_logger(name: str = None) -> logging.Logger:
    """Get a logger instance for the given name."""
    return logger.get_logger(name)


def set_log_level(level: int):
    """Set the global logging level."""
    logger.set_level(level)