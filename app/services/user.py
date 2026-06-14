from dataclasses import dataclass
from typing import Optional
from app.services.auth import auth_service


@dataclass
class User:
    id: str
    email: str
    is_pro: bool = False


class UserService:
    def __init__(self):
        self._user: Optional[User] = None

    def get_user(self) -> Optional[User]:
        """Get the current user."""
        auth_user = auth_service.get_user()
        if auth_user:
            # In a real app, we would fetch the user's PRO status from the database
            # For now, we'll return a basic user object
            return User(
                id=auth_user.id,
                email=auth_user.email,
                is_pro=False  # Would be fetched from database in real implementation
            )
        return None

    def set_user_pro(self, is_pro: bool) -> None:
        """Set the user's PRO status."""
        auth_user = auth_service.get_user()
        if auth_user:
            # In a real app, we would update the user's PRO status in the database
            # For now, we'll just note that this would happen
            pass

    def is_user_pro(self) -> bool:
        """Check if the current user has PRO status."""
        auth_user = auth_service.get_user()
        if auth_user:
            # In a real app, we would check the user's PRO status from the database
            # For now, we'll return False as default
            return False
        return False


# Global user service instance
current_user = UserService()