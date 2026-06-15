"""In-memory authentication repository useful for tests and local demo wiring."""

from src.domain.user import User


class InMemoryUserRepository:
    """Simple user repository adapter until persistent user management is introduced."""

    def __init__(self, users: list[User]) -> None:
        self._users_by_email = {user.email.lower(): user for user in users if user.is_active}

    def find_active_by_email(self, email: str) -> User | None:
        """Find an active user by normalized email address."""

        return self._users_by_email.get(email.lower())
