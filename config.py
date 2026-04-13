import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


def _to_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "MediaHub Downloader")
    app_env: str = os.getenv("APP_ENV", "development")
    session_file: str = os.getenv("SESSION_FILE", "session.txt")

    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_key: str = os.getenv("SUPABASE_KEY", "")

    stripe_secret_key: str = os.getenv("STRIPE_SECRET_KEY", "")
    stripe_publishable_key: str = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
    stripe_price_id: str = os.getenv("STRIPE_PRICE_ID", "")

    razorpay_key_id: str = os.getenv("RAZORPAY_KEY_ID", "")
    razorpay_key_secret: str = os.getenv("RAZORPAY_KEY_SECRET", "")

    dev_mode: bool = _to_bool(os.getenv("DEV_MODE"), default=True)


settings = Settings()
