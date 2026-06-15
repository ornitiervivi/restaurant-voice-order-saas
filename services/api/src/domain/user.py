"""User domain model and authorization rules."""

from dataclasses import dataclass
from enum import StrEnum


class UserRole(StrEnum):
    """Supported restaurant-scoped user roles."""

    ADMIN = "admin"
    WAITER = "waiter"
    KITCHEN = "kitchen"
    BAR = "bar"


@dataclass(frozen=True)
class User:
    """Authenticated application user scoped to a restaurant tenant."""

    id: int
    restaurant_id: int
    email: str
    full_name: str
    role: UserRole
    password_hash: str
    is_active: bool = True

    def can_access_restaurant(self, restaurant_id: int) -> bool:
        """Return whether this user belongs to the requested restaurant."""

        return self.is_active and self.restaurant_id == restaurant_id

    def has_role(self, *roles: UserRole) -> bool:
        """Return whether this active user has one of the allowed roles."""

        return self.is_active and self.role in roles
