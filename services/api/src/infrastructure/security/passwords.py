"""Password hashing helpers based on PBKDF2-HMAC-SHA256."""

import base64
import hashlib
import hmac
import os

_ALGORITHM = "pbkdf2_sha256"
_ITERATIONS = 210_000
_SALT_BYTES = 16


class Pbkdf2PasswordHasher:
    """Hash and verify passwords without storing plaintext credentials."""

    def hash(self, plain_password: str) -> str:
        salt = os.urandom(_SALT_BYTES)
        digest = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt, _ITERATIONS)
        return "$".join(
            [
                _ALGORITHM,
                str(_ITERATIONS),
                base64.urlsafe_b64encode(salt).decode("ascii"),
                base64.urlsafe_b64encode(digest).decode("ascii"),
            ]
        )

    def verify(self, plain_password: str, password_hash: str) -> bool:
        try:
            algorithm, iterations, encoded_salt, encoded_digest = password_hash.split("$", maxsplit=3)
            if algorithm != _ALGORITHM:
                return False
            salt = base64.urlsafe_b64decode(encoded_salt.encode("ascii"))
            expected_digest = base64.urlsafe_b64decode(encoded_digest.encode("ascii"))
            actual_digest = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt, int(iterations))
        except (ValueError, TypeError):
            return False

        return hmac.compare_digest(actual_digest, expected_digest)
