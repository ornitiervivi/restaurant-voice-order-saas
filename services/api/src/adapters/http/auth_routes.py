"""HTTP routes for email/password authentication."""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from src.application.auth.memory import InMemoryUserRepository
from src.application.auth.use_cases import AuthenticateUser, AuthenticationError
from src.domain.user import User, UserRole
from src.infrastructure.security.passwords import Pbkdf2PasswordHasher
from src.infrastructure.security.tokens import HmacJwtTokenIssuer
from src.infrastructure.settings import get_settings

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    """Credentials supplied by a user."""

    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=1, max_length=256)


class AuthenticatedUserResponse(BaseModel):
    """Public authenticated user profile."""

    id: int
    restaurant_id: int
    email: str = Field(min_length=3, max_length=254)
    full_name: str
    role: UserRole


class LoginResponse(BaseModel):
    """Token response for successful authentication."""

    access_token: str
    refresh_token: str
    token_type: str
    user: AuthenticatedUserResponse


def _build_authenticator() -> AuthenticateUser:
    settings = get_settings()
    passwords = Pbkdf2PasswordHasher()
    demo_user = User(
        id=1,
        restaurant_id=1,
        email="admin@demo.local",
        full_name="Demo Admin",
        role=UserRole.ADMIN,
        password_hash=passwords.hash("demo-admin-password"),
    )
    return AuthenticateUser(
        users=InMemoryUserRepository([demo_user]),
        passwords=passwords,
        tokens=HmacJwtTokenIssuer(settings),
    )


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest) -> LoginResponse:
    """Authenticate credentials and return JWT tokens for valid active users."""

    try:
        session = _build_authenticator().execute(payload.email, payload.password)
    except AuthenticationError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    return LoginResponse(
        access_token=session.access_token,
        refresh_token=session.refresh_token,
        token_type=session.token_type,
        user=AuthenticatedUserResponse(
            id=session.user.id,
            restaurant_id=session.user.restaurant_id,
            email=session.user.email,
            full_name=session.user.full_name,
            role=session.user.role,
        ),
    )
