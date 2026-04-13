import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


def _to_bool(value, default=False):
    if value is None:
        return default
    return value.lower() in ("true", "1", "yes")


@dataclass(frozen=True)
class Settings:
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_key: str = os.getenv("SUPABASE_KEY", "")

    stripe_secret_key: str = os.getenv("STRIPE_SECRET_KEY", "")
    stripe_price_id: str = os.getenv("STRIPE_PRICE_ID", "")
    stripe_success_url: str = os.getenv("STRIPE_SUCCESS_URL", "http://localhost/success")
    stripe_cancel_url: str = os.getenv("STRIPE_CANCEL_URL", "http://localhost/cancel")

    razorpay_key_id: str = os.getenv("RAZORPAY_KEY_ID", "")
    razorpay_key_secret: str = os.getenv("RAZORPAY_KEY_SECRET", "")

    session_file: str = os.getenv("SESSION_FILE", "session.txt")

    # 🔒 SECURITY FIX (IMPORTANT)
    dev_mode: bool = _to_bool(os.getenv("DEV_MODE"), False)


settings = Settings()
