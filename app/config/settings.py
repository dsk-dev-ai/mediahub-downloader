import os
import sys
from dataclasses import dataclass
from dotenv import load_dotenv

if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(__file__)

load_dotenv(os.path.join(base_path, ".env"))


def _to_bool(value, default=False):
    if value is None:
        return default
    return value.lower() in ("true", "1", "yes")


@dataclass(frozen=True)
class Settings:
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_key: str = os.getenv("SUPABASE_KEY", "")

    session_file: str = os.getenv("SESSION_FILE", "session.txt")

    dev_mode: bool = _to_bool(os.getenv("DEV_MODE"), False)


settings = Settings()