from dataclasses import dataclass
from typing import Optional

from supabase import create_client

from config import settings


@dataclass
class SessionUser:
    id: str
    email: str


class AuthService:
    def __init__(self):
        self.user: Optional[SessionUser] = None
        self.client = None

        if settings.supabase_url and settings.supabase_key:
            self.client = create_client(settings.supabase_url, settings.supabase_key)

    def signup(self, email, password):
        if settings.dev_mode:
            self.user = SessionUser(id="dev-user", email=email)
            return True, "✅ Dev signup success"

        if not self.client:
            return False, "❌ Supabase is not configured"

        try:
            if not email or not password:
                return False, "❌ Email & password required"

            res = self.client.auth.sign_up({"email": email, "password": password})

            if res.user:
                self.client.table("profiles").insert(
                    {"id": res.user.id, "email": email, "is_pro": False}
                ).execute()

                self.user = SessionUser(id=res.user.id, email=email)
                return True, "✅ Signup successful"

            return False, "❌ Signup failed"

        except Exception as e:
            error = str(e).lower()
            if "rate limit" in error:
                return False, "⏳ Too many attempts. Wait 1 min."
            return False, f"❌ {str(e)}"

    def login(self, email, password):
        if settings.dev_mode:
            self.user = SessionUser(id="dev-user", email=email)
            return True, "✅ Dev login success"

        if not self.client:
            return False, "❌ Supabase is not configured"

        try:
            if not email or not password:
                return False, "❌ Email & password required"

            res = self.client.auth.sign_in_with_password({"email": email, "password": password})

            if res.user:
                self.user = SessionUser(id=res.user.id, email=res.user.email)
                return True, "✅ Login successful"

            return False, "❌ Invalid credentials"

        except Exception as e:
            error = str(e).lower()
            if "email not confirmed" in error:
                return False, "📧 Please verify your email first"
            if "invalid login credentials" in error:
                return False, "❌ Wrong email or password"
            if "rate limit" in error:
                return False, "⏳ Too many attempts. Wait 1 min."
            return False, f"❌ {str(e)}"

    def get_user(self):
        return self.user


auth_service = AuthService()
