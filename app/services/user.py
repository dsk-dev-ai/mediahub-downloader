from app.services.supabase_client import db_select
from app.services.auth import auth_service


class User:
    def __init__(self) -> None:
        self.is_pro: bool = False

    def load(self) -> None:
        user = auth_service.get_user()
        if not user:
            return

        try:
            res = db_select("profiles", f"&id=eq.{user.id}")
            if res:
                self.is_pro = bool(res[0].get("is_pro", False))
        except Exception:
            self.is_pro = False


current_user = User()