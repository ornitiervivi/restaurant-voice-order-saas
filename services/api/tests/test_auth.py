"""Authentication and role authorization tests."""

import base64
import json

import pytest

from src.application.auth.use_cases import AuthenticateUser, AuthenticationError, AuthorizationError, AuthorizeRestaurantRole
from src.application.auth.memory import InMemoryUserRepository
from src.domain.user import User, UserRole
from src.infrastructure.security.passwords import Pbkdf2PasswordHasher
from src.infrastructure.security.tokens import HmacJwtTokenIssuer


class _Secret:
    def get_secret_value(self) -> str:
        return "test-secret"


class _TokenSettings:
    jwt_secret = _Secret()
    access_token_ttl_minutes = 15
    refresh_token_ttl_minutes = 60


def _decode_payload(token: str) -> dict[str, object]:
    payload = token.split(".")[1]
    payload += "=" * (-len(payload) % 4)
    return json.loads(base64.urlsafe_b64decode(payload.encode("ascii")))


def test_passwords_are_hashed_and_verified() -> None:
    hasher = Pbkdf2PasswordHasher()

    password_hash = hasher.hash("secret-password")

    assert password_hash != "secret-password"
    assert password_hash.startswith("pbkdf2_sha256$")
    assert hasher.verify("secret-password", password_hash)
    assert not hasher.verify("wrong-password", password_hash)


def test_authenticate_user_issues_restaurant_scoped_tokens_for_valid_credentials() -> None:
    hasher = Pbkdf2PasswordHasher()
    user = User(
        id=10,
        restaurant_id=20,
        email="waiter@example.test",
        full_name="Waiter Example",
        role=UserRole.WAITER,
        password_hash=hasher.hash("correct-password"),
    )
    authenticator = AuthenticateUser(
        users=InMemoryUserRepository([user]),
        passwords=hasher,
        tokens=HmacJwtTokenIssuer(_TokenSettings()),
    )

    session = authenticator.execute(" WAITER@example.test ", "correct-password")

    assert session.token_type == "bearer"
    access_payload = _decode_payload(session.access_token)
    assert access_payload["sub"] == "10"
    assert access_payload["restaurant_id"] == 20
    assert access_payload["role"] == "waiter"
    assert access_payload["typ"] == "access"


def test_invalid_credentials_fail_safely() -> None:
    hasher = Pbkdf2PasswordHasher()
    user = User(
        id=10,
        restaurant_id=20,
        email="waiter@example.test",
        full_name="Waiter Example",
        role=UserRole.WAITER,
        password_hash=hasher.hash("correct-password"),
    )
    authenticator = AuthenticateUser(
        users=InMemoryUserRepository([user]),
        passwords=hasher,
        tokens=HmacJwtTokenIssuer(_TokenSettings()),
    )

    with pytest.raises(AuthenticationError, match="Invalid email or password"):
        authenticator.execute("waiter@example.test", "wrong-password")

    with pytest.raises(AuthenticationError, match="Invalid email or password"):
        authenticator.execute("missing@example.test", "correct-password")


def test_role_and_restaurant_scoping_are_enforced() -> None:
    user = User(
        id=10,
        restaurant_id=20,
        email="waiter@example.test",
        full_name="Waiter Example",
        role=UserRole.WAITER,
        password_hash="unused",
    )
    authorizer = AuthorizeRestaurantRole()

    authorizer.execute(user, restaurant_id=20, allowed_roles={UserRole.WAITER, UserRole.ADMIN})

    with pytest.raises(AuthorizationError):
        authorizer.execute(user, restaurant_id=999, allowed_roles={UserRole.WAITER})

    with pytest.raises(AuthorizationError):
        authorizer.execute(user, restaurant_id=20, allowed_roles={UserRole.ADMIN})


def test_login_endpoint_accepts_valid_demo_credentials() -> None:
    pytest.importorskip("fastapi")
    TestClient = pytest.importorskip("fastapi.testclient").TestClient
    from src.main import create_app

    client = TestClient(create_app())

    response = client.post(
        "/auth/login",
        json={"email": "admin@demo.local", "password": "demo-admin-password"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert body["refresh_token"]
    assert body["user"] == {
        "id": 1,
        "restaurant_id": 1,
        "email": "admin@demo.local",
        "full_name": "Demo Admin",
        "role": "admin",
    }


def test_login_endpoint_rejects_invalid_credentials() -> None:
    pytest.importorskip("fastapi")
    TestClient = pytest.importorskip("fastapi.testclient").TestClient
    from src.main import create_app

    client = TestClient(create_app())

    response = client.post(
        "/auth/login",
        json={"email": "admin@demo.local", "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid email or password."}
