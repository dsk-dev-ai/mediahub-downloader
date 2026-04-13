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
    dev_mode: bool = _to_bool(os.getenv("DEV_MODE"), True)


settings = Settings()
