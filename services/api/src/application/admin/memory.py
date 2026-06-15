"""In-memory admin repository for tests and local demo routes."""

from dataclasses import replace

from src.application.admin.use_cases import AdminNotFoundError
from src.domain.admin import Product, RestaurantProfile, RestaurantTable, Station
from src.domain.user import User, UserRole


class InMemoryAdminRepository:
    """Tenant-aware in-memory setup repository."""

    def __init__(self) -> None:
        self.restaurants = {1: RestaurantProfile(1, "Demo Restaurant", "demo")}
        self.users = {1: [User(1, 1, "admin@demo.local", "Demo Admin", UserRole.ADMIN, "demo-hash")]}
        self.tables: dict[int, list[RestaurantTable]] = {1: []}
        self.products: dict[int, list[Product]] = {1: []}
        self._next_user_id = 2
        self._next_table_id = 1
        self._next_product_id = 1

    def get_restaurant(self, restaurant_id: int) -> RestaurantProfile | None:
        return self.restaurants.get(restaurant_id)

    def update_restaurant(self, restaurant_id: int, name: str, slug: str) -> RestaurantProfile:
        current = self.restaurants.get(restaurant_id)
        if current is None:
            raise AdminNotFoundError("Restaurant not found.")
        updated = replace(current, name=name, slug=slug)
        self.restaurants[restaurant_id] = updated
        return updated

    def list_users(self, restaurant_id: int) -> list[User]:
        return list(self.users.get(restaurant_id, []))

    def create_user(self, restaurant_id: int, email: str, full_name: str, role: UserRole, password_hash: str) -> User:
        user = User(self._next_user_id, restaurant_id, email, full_name, role, password_hash)
        self._next_user_id += 1
        self.users.setdefault(restaurant_id, []).append(user)
        return user

    def update_user(self, restaurant_id: int, user_id: int, full_name: str | None, role: UserRole | None) -> User:
        users = self.users.get(restaurant_id, [])
        for index, user in enumerate(users):
            if user.id == user_id:
                updated = replace(user, full_name=full_name or user.full_name, role=role or user.role)
                users[index] = updated
                return updated
        raise AdminNotFoundError("User not found.")

    def deactivate_user(self, restaurant_id: int, user_id: int) -> User:
        users = self.users.get(restaurant_id, [])
        for index, user in enumerate(users):
            if user.id == user_id:
                updated = replace(user, is_active=False)
                users[index] = updated
                return updated
        raise AdminNotFoundError("User not found.")

    def list_tables(self, restaurant_id: int) -> list[RestaurantTable]:
        return list(self.tables.get(restaurant_id, []))

    def create_table(self, restaurant_id: int, label: str) -> RestaurantTable:
        table = RestaurantTable(self._next_table_id, restaurant_id, label)
        self._next_table_id += 1
        self.tables.setdefault(restaurant_id, []).append(table)
        return table

    def update_table(self, restaurant_id: int, table_id: int, label: str | None, is_active: bool | None) -> RestaurantTable:
        tables = self.tables.get(restaurant_id, [])
        for index, table in enumerate(tables):
            if table.id == table_id:
                updated = replace(table, label=label or table.label, is_active=table.is_active if is_active is None else is_active)
                tables[index] = updated
                return updated
        raise AdminNotFoundError("Table not found.")

    def list_products(self, restaurant_id: int) -> list[Product]:
        return list(self.products.get(restaurant_id, []))

    def create_product(self, restaurant_id: int, name: str, station: Station, price_cents: int) -> Product:
        product = Product(self._next_product_id, restaurant_id, name, station, price_cents)
        self._next_product_id += 1
        self.products.setdefault(restaurant_id, []).append(product)
        return product

    def update_product(self, restaurant_id: int, product_id: int, name: str | None, station: Station | None, price_cents: int | None, is_available: bool | None) -> Product:
        products = self.products.get(restaurant_id, [])
        for index, product in enumerate(products):
            if product.id == product_id:
                updated = replace(
                    product,
                    name=name or product.name,
                    station=station or product.station,
                    price_cents=product.price_cents if price_cents is None else price_cents,
                    is_available=product.is_available if is_available is None else is_available,
                )
                products[index] = updated
                return updated
        raise AdminNotFoundError("Product not found.")
