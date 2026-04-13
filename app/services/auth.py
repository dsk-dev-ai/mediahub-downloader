from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

# 🔧 TURN ON FOR TESTING (VERY IMPORTANT)
DEV_MODE = True


class AuthService:
    def __init__(self):
        self.client = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.user = None

    # ========================
    # 📝 SIGNUP
    # ========================
    def signup(self, email, password):
        if DEV_MODE:
            print("DEV SIGNUP")
            return True, "✅ Dev signup success"

        try:
            if not email or not password:
                return False, "❌ Email & password required"

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

                return True, "✅ Signup successful"

            return False, "❌ Signup failed"

        except Exception as e:
            error = str(e).lower()

            if "rate limit" in error:
                return False, "⏳ Too many attempts. Wait 1 min."

            return False, f"❌ {str(e)}"

    # ========================
    # 🔐 LOGIN
    # ========================
    def login(self, email, password):
        if DEV_MODE:
            print("DEV LOGIN")
            # 👇 THIS FIXES YOUR ISSUE
            self.user = type("User", (), {"email": email})
            return True, "✅ Dev login success"

        try:
            if not email or not password:
                return False, "❌ Email & password required"

            res = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            if res.user:
                self.user = res.user
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