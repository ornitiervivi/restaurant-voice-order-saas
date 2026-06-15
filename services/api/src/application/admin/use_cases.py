"""Admin setup CRUD use cases."""

from typing import Protocol

from src.application.auth.use_cases import AuthorizeRestaurantRole
from src.domain.admin import Product, RestaurantProfile, RestaurantTable, Station
from src.domain.user import User, UserRole


class AdminRepository(Protocol):
    """Persistence port for restaurant setup data."""

    def get_restaurant(self, restaurant_id: int) -> RestaurantProfile | None: ...
    def update_restaurant(self, restaurant_id: int, name: str, slug: str) -> RestaurantProfile: ...
    def list_users(self, restaurant_id: int) -> list[User]: ...
    def create_user(self, restaurant_id: int, email: str, full_name: str, role: UserRole, password_hash: str) -> User: ...
    def update_user(self, restaurant_id: int, user_id: int, full_name: str | None, role: UserRole | None) -> User: ...
    def deactivate_user(self, restaurant_id: int, user_id: int) -> User: ...
    def list_tables(self, restaurant_id: int) -> list[RestaurantTable]: ...
    def create_table(self, restaurant_id: int, label: str) -> RestaurantTable: ...
    def update_table(self, restaurant_id: int, table_id: int, label: str | None, is_active: bool | None) -> RestaurantTable: ...
    def list_products(self, restaurant_id: int) -> list[Product]: ...
    def create_product(self, restaurant_id: int, name: str, station: Station, price_cents: int) -> Product: ...
    def update_product(self, restaurant_id: int, product_id: int, name: str | None, station: Station | None, price_cents: int | None, is_available: bool | None) -> Product: ...


class AdminNotFoundError(Exception):
    """Raised when a tenant-scoped admin resource does not exist."""


class ManageRestaurantSetup:
    """Admin-only use case boundary for restaurant setup CRUD."""

    def __init__(self, repository: AdminRepository) -> None:
        self._repository = repository
        self._authorize = AuthorizeRestaurantRole()

    def _ensure_admin(self, actor: User, restaurant_id: int) -> None:
        self._authorize.execute(actor, restaurant_id, {UserRole.ADMIN})

    def get_restaurant(self, actor: User, restaurant_id: int) -> RestaurantProfile:
        self._ensure_admin(actor, restaurant_id)
        restaurant = self._repository.get_restaurant(restaurant_id)
        if restaurant is None:
            raise AdminNotFoundError("Restaurant not found.")
        return restaurant

    def update_restaurant(self, actor: User, restaurant_id: int, name: str, slug: str) -> RestaurantProfile:
        self._ensure_admin(actor, restaurant_id)
        return self._repository.update_restaurant(restaurant_id, name, slug)

    def list_users(self, actor: User, restaurant_id: int) -> list[User]:
        self._ensure_admin(actor, restaurant_id)
        return self._repository.list_users(restaurant_id)

    def create_user(self, actor: User, restaurant_id: int, email: str, full_name: str, role: UserRole, password_hash: str) -> User:
        self._ensure_admin(actor, restaurant_id)
        return self._repository.create_user(restaurant_id, email.strip().lower(), full_name, role, password_hash)

    def update_user(self, actor: User, restaurant_id: int, user_id: int, full_name: str | None, role: UserRole | None) -> User:
        self._ensure_admin(actor, restaurant_id)
        return self._repository.update_user(restaurant_id, user_id, full_name, role)

    def deactivate_user(self, actor: User, restaurant_id: int, user_id: int) -> User:
        self._ensure_admin(actor, restaurant_id)
        return self._repository.deactivate_user(restaurant_id, user_id)

    def list_tables(self, actor: User, restaurant_id: int) -> list[RestaurantTable]:
        self._ensure_admin(actor, restaurant_id)
        return self._repository.list_tables(restaurant_id)

    def create_table(self, actor: User, restaurant_id: int, label: str) -> RestaurantTable:
        self._ensure_admin(actor, restaurant_id)
        return self._repository.create_table(restaurant_id, label)

    def update_table(self, actor: User, restaurant_id: int, table_id: int, label: str | None, is_active: bool | None) -> RestaurantTable:
        self._ensure_admin(actor, restaurant_id)
        return self._repository.update_table(restaurant_id, table_id, label, is_active)

    def list_products(self, actor: User, restaurant_id: int) -> list[Product]:
        self._ensure_admin(actor, restaurant_id)
        return self._repository.list_products(restaurant_id)

    def create_product(self, actor: User, restaurant_id: int, name: str, station: Station, price_cents: int) -> Product:
        self._ensure_admin(actor, restaurant_id)
        return self._repository.create_product(restaurant_id, name, station, price_cents)

    def update_product(self, actor: User, restaurant_id: int, product_id: int, name: str | None, station: Station | None, price_cents: int | None, is_available: bool | None) -> Product:
        self._ensure_admin(actor, restaurant_id)
        return self._repository.update_product(restaurant_id, product_id, name, station, price_cents, is_available)
