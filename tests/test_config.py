"""Tests for configuration module."""
import os
from pathlib import Path
import sys

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Settings


def test_settings_defaults():
    """Test that settings have proper defaults."""
    # Clear relevant environment variables
    for var in ["SUPABASE_URL", "SUPABASE_KEY", "STRIPE_SECRET_KEY", 
                "STRIPE_PRICE_ID", "STRIPE_SUCCESS_URL", "STRIPE_CANCEL_URL",
                "RAZORPAY_KEY_ID", "RAZORPAY_KEY_SECRET", "SESSION_FILE", "DEV_MODE"]:
        if var in os.environ:
            del os.environ[var]
    
    settings = Settings()
    
    # Check defaults
    assert settings.supabase_url == ""
    assert settings.supabase_key == ""
    assert settings.stripe_secret_key == ""
    assert settings.stripe_price_id == ""
    assert settings.stripe_success_url == "http://localhost/success"
    assert settings.stripe_cancel_url == "http://localhost/cancel"
    assert settings.razorpay_key_id == ""
    assert settings.razorpay_key_secret == ""
    assert settings.session_file == "session.txt"
    assert settings.dev_mode is False


def test_settings_from_env():
    """Test that settings read from environment variables."""
    os.environ["SUPABASE_URL"] = "https://test.example.com"
    os.environ["SUPABASE_KEY"] = "test-key"
    os.environ["STRIPE_SECRET_KEY"] = "sk_test_123"
    os.environ["STRIPE_PRICE_ID"] = "price_123"
    os.environ["STRIPE_SUCCESS_URL"] = "https://example.com/success"
    os.environ["STRIPE_CANCEL_URL"] = "https://example.com/cancel"
    os.environ["RAZORPAY_KEY_ID"] = "rzp_test_123"
    os.environ["RAZORPAY_KEY_SECRET"] = "rzp_secret_123"
    os.environ["SESSION_FILE"] = "custom_session.txt"
    os.environ["DEV_MODE"] = "true"
    
    try:
        settings = Settings()
        
        assert settings.supabase_url == "https://test.example.com"
        assert settings.supabase_key == "test-key"
        assert settings.stripe_secret_key == "sk_test_123"
        assert settings.stripe_price_id == "price_123"
        assert settings.stripe_success_url == "https://example.com/success"
        assert settings.stripe_cancel_url == "https://example.com/cancel"
        assert settings.razorpay_key_id == "rzp_test_123"
        assert settings.razorpay_key_secret == "rzp_secret_123"
        assert settings.session_file == "custom_session.txt"
        assert settings.dev_mode is True
    finally:
        # Clean up environment variables
        for var in ["SUPABASE_URL", "SUPABASE_KEY", "STRIPE_SECRET_KEY", 
                    "STRIPE_PRICE_ID", "STRIPE_SUCCESS_URL", "STRIPE_CANCEL_URL",
                    "RAZORPAY_KEY_ID", "RAZORPAY_KEY_SECRET", "SESSION_FILE", "DEV_MODE"]:
            if var in os.environ:
                del os.environ[var]