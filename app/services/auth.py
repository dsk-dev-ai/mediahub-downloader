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
            return True, "✅ Dev signup"

        if not self.client:
            return False, "❌ Supabase not configured"

        try:
            res = self.client.auth.sign_up({
                "email": email,
                "password": password
            })

            if res.user:
                self.client.table("profiles").insert({
                    "id": res.user.id,
                    "email": email,
                    "is_pro": False
                }).execute()

                self.user = SessionUser(id=res.user.id, email=email)
                return True, "✅ Signup success"

            return False, "❌ Signup failed"

        except Exception as e:
            return False, str(e)

    def login(self, email, password):
        if settings.dev_mode:
            self.user = SessionUser(id="dev-user", email=email)
            return True, "✅ Dev login"

        # ✅ ONLY FIX ADDED (prevents crash)
        if not self.client:
            return False, "❌ Supabase not configured"

        try:
            res = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            if res.user:
                self.user = SessionUser(id=res.user.id, email=res.user.email)
                return True, "✅ Login success"

            return False, "❌ Invalid credentials"

        except Exception as e:
            return False, str(e)

    def get_user(self):
        return self.user


auth_service = AuthService()
