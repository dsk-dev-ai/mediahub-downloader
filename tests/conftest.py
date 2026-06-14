"""Pytest configuration file."""
import os
import sys
import tempfile
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_env(monkeypatch):
    """Mock environment variables for testing."""
    monkeypatch.setenv("SUPABASE_URL", "https://test.supabase.co")
    monkeypatch.setenv("SUPABASE_KEY", "test-key")
    monkeypatch.setenv("STRIPE_SECRET_KEY", "sk_test_...")
    monkeypatch.setenv("STRIPE_PRICE_ID", "price_test_...")
    monkeypatch.setenv("STRIPE_SUCCESS_URL", "http://localhost/success")
    monkeypatch.setenv("STRIPE_CANCEL_URL", "http://localhost/cancel")
    monkeypatch.setenv("RAZORPAY_KEY_ID", "test_key_id")
    monkeypatch.setenv("RAZORPAY_KEY_SECRET", "test_key_secret")
    monkeypatch.setenv("DEV_MODE", "true")
    monkeypatch.setenv("SESSION_FILE", "test_session.txt")