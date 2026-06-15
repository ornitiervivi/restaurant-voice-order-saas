"""Minimal signed JWT issuer for MVP authentication."""

import base64
import hashlib
import hmac
import json
import time
from typing import Any

from src.domain.user import User


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


class HmacJwtTokenIssuer:
    """Issue HS256 JWT access and refresh tokens with tenant and role claims."""

    def __init__(self, settings: object) -> None:
        self._secret = settings.jwt_secret.get_secret_value().encode("utf-8")
        self._access_ttl_seconds = settings.access_token_ttl_minutes * 60
        self._refresh_ttl_seconds = settings.refresh_token_ttl_minutes * 60

    def issue_access_token(self, user: User) -> str:
        return self._issue(user, token_use="access", ttl_seconds=self._access_ttl_seconds)

    def issue_refresh_token(self, user: User) -> str:
        return self._issue(user, token_use="refresh", ttl_seconds=self._refresh_ttl_seconds)

    def _issue(self, user: User, token_use: str, ttl_seconds: int) -> str:
        now = int(time.time())
        payload: dict[str, Any] = {
            "sub": str(user.id),
            "restaurant_id": user.restaurant_id,
            "role": user.role.value,
            "email": user.email,
            "typ": token_use,
            "iat": now,
            "exp": now + ttl_seconds,
        }
        header = {"alg": "HS256", "typ": "JWT"}
        signing_input = ".".join(
            [
                _b64url(json.dumps(header, separators=(",", ":")).encode("utf-8")),
                _b64url(json.dumps(payload, separators=(",", ":")).encode("utf-8")),
            ]
        )
        signature = hmac.new(self._secret, signing_input.encode("ascii"), hashlib.sha256).digest()
        return f"{signing_input}.{_b64url(signature)}"
