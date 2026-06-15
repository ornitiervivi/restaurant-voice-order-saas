"""Authentication and authorization use cases."""

from dataclasses import dataclass
from typing import Protocol

from src.domain.user import User, UserRole


class AuthenticationError(Exception):
    """Raised when credentials are invalid or the user cannot authenticate."""


class AuthorizationError(Exception):
    """Raised when an authenticated user is not allowed to perform an action."""


class UserRepository(Protocol):
    """Persistence port for user authentication lookups."""

    def find_active_by_email(self, email: str) -> User | None:
        """Return an active user for the normalized email, if one exists."""


class PasswordVerifier(Protocol):
    """Infrastructure port for password hash verification."""

    def verify(self, plain_password: str, password_hash: str) -> bool:
        """Return whether a plaintext password matches the stored hash."""


class TokenIssuer(Protocol):
    """Infrastructure port for issuing access and refresh tokens."""

    def issue_access_token(self, user: User) -> str:
        """Issue a short-lived access token for the authenticated user."""

    def issue_refresh_token(self, user: User) -> str:
        """Issue a refresh token for the authenticated user."""


@dataclass(frozen=True)
class AuthenticatedSession:
    """Token response returned after successful login."""

    access_token: str
    refresh_token: str
    token_type: str
    user: User


class AuthenticateUser:
    """Authenticate email/password credentials without leaking failure reasons."""

    def __init__(self, users: UserRepository, passwords: PasswordVerifier, tokens: TokenIssuer) -> None:
        self._users = users
        self._passwords = passwords
        self._tokens = tokens

    def execute(self, email: str, password: str) -> AuthenticatedSession:
        normalized_email = email.strip().lower()
        user = self._users.find_active_by_email(normalized_email)
        if user is None or not self._passwords.verify(password, user.password_hash):
            raise AuthenticationError("Invalid email or password.")

        return AuthenticatedSession(
            access_token=self._tokens.issue_access_token(user),
            refresh_token=self._tokens.issue_refresh_token(user),
            token_type="bearer",
            user=user,
        )


class AuthorizeRestaurantRole:
    """Authorize a user for a restaurant tenant and at least one role."""

    def execute(self, user: User, restaurant_id: int, allowed_roles: set[UserRole]) -> None:
        if not user.can_access_restaurant(restaurant_id) or not user.has_role(*allowed_roles):
            raise AuthorizationError("User is not authorized for this restaurant action.")
