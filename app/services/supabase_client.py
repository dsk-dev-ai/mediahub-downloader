import httpx
from config import SUPABASE_URL, SUPABASE_KEY

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}


def db_insert(table, data):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    return httpx.post(url, json=data, headers=headers)


def db_select(table, query=""):
    url = f"{SUPABASE_URL}/rest/v1/{table}?select=*{query}"
    return httpx.get(url, headers=headers).json()


def db_update(table, data, condition):
    url = f"{SUPABASE_URL}/rest/v1/{table}?{condition}"
    return httpx.patch(url, json=data, headers=headers)