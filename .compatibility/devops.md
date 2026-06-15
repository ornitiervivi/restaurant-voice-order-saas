# DevOps compatibility

Track Docker, Compose, CI/CD, deployment platform and runtime version constraints here.

## T-003 local Compose baseline

- Docker Compose file: `infra/docker-compose.yml`.
- PostgreSQL runs as the default local service.
- API development container is behind the optional `api` Compose profile; full production-style API containerization remains deferred to T-020.
