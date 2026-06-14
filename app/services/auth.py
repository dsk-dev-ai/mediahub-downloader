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
            self.user = SessionUser(id=\"dev-user\", email=email)
            return True, \"✅ Dev signup\"

        if not self.client:
            return False, \"❌ Supabase not configured\"

        if not email or not password:
            return False, \"❌ Email & password required\"

        # Input validation and sanitization
        email = email.strip().lower()
        if not email or len(email) > 254:
            return False, \"❌ Invalid email address\"
        
        # Basic email format validation
        if \"@\" not in email or \".\" not in email.split(\"@\")[-1]:
            return False, \"❌ Invalid email format\"
            
        if not password or len(password) < 6:
            return False, \"❼ Password must be at least 6 characters long\"
        if len(password) > 128:
            return False, \"❼ Password too long (maximum 128 characters)\"

        try:
            res = self.client.auth.sign_up({\n                \"email\": email,\n                \"password\": password\n            })

            if res.user:
                self.client.table(\"profiles\").insert({\n                    \"id\": res.user.id,\n                    \"email\": email,\n                    \"is_pro\": False\n                }).execute()

                self.user = SessionUser(id=res.user.id, email=email)
                return True, \"✅ Signup success\"

            return False, \"❌ Signup failed\"

        except Exception as e:
            return False, str(e)   # ✅ FIXED (single clean return)

    def login(self, email, password):
        if settings.dev_mode:
            self.user = SessionUser(id=\"dev-user\", email=email)
            return True, \"✅ Dev login\"\n\n        # ✅ CRITICAL FIX (bot issue resolved)\n        if not self.client:\n            return False, \"❌ Supabase not configured\"\n\n        if not email or not password:\n            return False, \"❌ Email & password required\"\n\n        # Input validation and sanitization
        email = email.strip().lower()
        if not email or len(email) > 254:
            return False, \"❌ Invalid email address\"
        
        # Basic email format validation
        if \"@\" not in email or \".\" not in email.split(\"@\")[-1]:
            return False, \"❌ Invalid email format\"
            
        if not password or len(password) < 6:
            return False, \"❼ Password must be at least 6 characters long\"
        if len(password) > 128:
            return False, \"❼ Password too long (maximum 128 characters)\"

        try:
            res = self.client.auth.sign_in_with_password({\n                \"email\": email,\n                \"password\": password\n            })\n\n            if res.user:\n                self.user = SessionUser(id=res.user.id, email=res.user.email)\n                return True, \"✅ Login success\"\n\n            return False, \"❌ Invalid credentials\"\n\n        except Exception as e:\n            return False, str(e)   # ✅ FIXED (no duplicate return)

    def get_user(self):
        return self.user


auth_service = AuthService()