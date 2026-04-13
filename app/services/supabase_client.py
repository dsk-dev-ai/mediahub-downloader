import httpx
from config import settings


def headers():
    return {
        "apikey": settings.supabase_key,
        "Authorization": f"Bearer {settings.supabase_key}",
        "Content-Type": "application/json",
    }


def db_update(table, data, condition):
    url = f"{settings.supabase_url}/rest/v1/{table}?{condition}"
    return httpx.patch(url, json=data, headers=headers())
