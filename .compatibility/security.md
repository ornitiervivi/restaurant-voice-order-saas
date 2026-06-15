# Security compatibility

Track authentication, authorization, secrets, dependency risk and tenant isolation constraints here.


## T-005 authentication baseline

- Passwords use PBKDF2-HMAC-SHA256 hashes with per-password random salts; plaintext passwords are never stored.
- Access and refresh tokens are signed HS256 JWTs containing user id, restaurant id, role, token type, issued-at and expiration claims.
- Authorization is implemented as an application use case that checks active user status, restaurant tenant scope and allowed role before protected actions.
- The HTTP route currently uses a local in-memory demo repository only until persistent user management is introduced in T-006; use-case ports are already repository-agnostic.
