import httpx
from config import settings


def headers() -> dict:
    return {
        "apikey": settings.supabase_key,
        "Authorization": f"Bearer {settings.supabase_key}",
        "Content-Type": "application/json",
    }


def db_update(table: str, data: dict, condition: str):
    url = f"{settings.supabase_url}/rest/v1/{table}?{condition}"
    return httpx.patch(url, json=data, headers=headers())


def db_select(table: str, condition: str):
    url = f"{settings.supabase_url}/rest/v1/{table}?{condition}"
    return httpx.get(url, headers=headers())


def db_insert(table: str, data: dict):
    url = f"{settings.supabase_url}/rest/v1/{table}"
    return httpx.post(url, json=data, headers=headers())