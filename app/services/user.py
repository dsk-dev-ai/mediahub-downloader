from app.services.supabase_client import db_select
from app.services.auth import auth_service


class User:
    def __init__(self):
        self.is_pro = False

    def load(self):
        user = auth_service.get_user()

        if not user:
            return

        res = db_select("profiles", f"&id=eq.{user['id']}")

        if res:
            self.is_pro = res[0]["is_pro"]


current_user = User()