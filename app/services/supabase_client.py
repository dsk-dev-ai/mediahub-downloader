import httpx

from config import settings

headers = {
    "apikey": settings.supabase_key,
    "Authorization": f"Bearer {settings.supabase_key}",
    "Content-Type": "application/json",
}


def _ensure_configured():
    if not settings.supabase_url or not settings.supabase_key:
        raise RuntimeError("Supabase is not configured. Set SUPABASE_URL and SUPABASE_KEY.")


def db_insert(table, data):
    _ensure_configured()
    url = f"{settings.supabase_url}/rest/v1/{table}"
    return httpx.post(url, json=data, headers=headers, timeout=20)


def db_select(table, query=""):
    _ensure_configured()
    url = f"{settings.supabase_url}/rest/v1/{table}?select=*{query}"
    return httpx.get(url, headers=headers, timeout=20).json()


def db_update(table, data, condition):
    _ensure_configured()
    url = f"{settings.supabase_url}/rest/v1/{table}?{condition}"
    return httpx.patch(url, json=data, headers=headers, timeout=20)
