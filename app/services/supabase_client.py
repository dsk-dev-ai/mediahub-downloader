from supabase import create_client
from config import settings


def get_supabase_client():
    """
    Get a Supabase client instance.
    
    Returns:
        Supabase client or None if not configured
    """
    if not settings.supabase_url or not settings.supabase_key:
        return None
    
    return create_client(settings.supabase_url, settings.supabase_key)


# Initialize client (can be None if not configured)
supabase_client = get_supabase_client()