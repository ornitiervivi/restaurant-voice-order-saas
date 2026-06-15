"""Order lifecycle use cases."""

from typing import Protocol

from src.application.auth.use_cases import AuthorizeRestaurantRole
from src.domain.admin import Product, RestaurantTable, Station
from src.domain.order import Order, OrderItem, OrderItemStatus, OrderStatus
from src.domain.user import User, UserRole


class OrderRepository(Protocol):
    """Persistence port for table order lifecycle data."""

    def get_table(self, restaurant_id: int, table_id: int) -> RestaurantTable | None: ...
    def get_product(self, restaurant_id: int, product_id: int) -> Product | None: ...
    def get_open_order_for_table(self, restaurant_id: int, table_id: int) -> Order | None: ...
    def create_order(self, restaurant_id: int, table_id: int, opened_by_user_id: int) -> Order: ...
    def get_order(self, restaurant_id: int, order_id: int) -> Order | None: ...
    def list_order_items(self, restaurant_id: int, order_id: int) -> list[OrderItem]: ...
    def get_order_item(self, restaurant_id: int, item_id: int) -> OrderItem | None: ...
    def add_confirmed_item(self, order: Order, product: Product, quantity: int, notes: str | None, confirmed_by_user_id: int) -> OrderItem: ...
    def update_item_status(self, restaurant_id: int, item_id: int, status: OrderItemStatus) -> OrderItem: ...
    def close_order(self, restaurant_id: int, order_id: int) -> Order: ...
    def list_table_history(self, restaurant_id: int, table_id: int) -> list[Order]: ...


class OrderNotFoundError(Exception):
    """Raised when a tenant-scoped order resource does not exist."""


class OrderStateError(Exception):
    """Raised when an order lifecycle transition is not allowed."""


class ManageOrders:
    """Use case boundary for waiter order lifecycle and station item status updates."""

    def __init__(self, repository: OrderRepository) -> None:
        self._repository = repository
        self._authorize = AuthorizeRestaurantRole()

    def open_or_resume_order(self, actor: User, restaurant_id: int, table_id: int) -> Order:
        self._authorize.execute(actor, restaurant_id, {UserRole.WAITER, UserRole.ADMIN})
        table = self._repository.get_table(restaurant_id, table_id)
        if table is None or not table.is_active:
            raise OrderNotFoundError("Active table not found.")
        existing = self._repository.get_open_order_for_table(restaurant_id, table_id)
        if existing is not None:
            return existing
        return self._repository.create_order(restaurant_id, table_id, actor.id)

    def add_confirmed_item(self, actor: User, restaurant_id: int, order_id: int, product_id: int, quantity: int, notes: str | None = None) -> OrderItem:
        self._authorize.execute(actor, restaurant_id, {UserRole.WAITER, UserRole.ADMIN})
        if quantity <= 0:
            raise OrderStateError("Confirmed item quantity must be greater than zero.")
        order = self._repository.get_order(restaurant_id, order_id)
        if order is None:
            raise OrderNotFoundError("Order not found.")
        if not order.can_accept_items():
            raise OrderStateError("Closed orders reject new confirmed items.")
        product = self._repository.get_product(restaurant_id, product_id)
        if product is None or not product.is_available:
            raise OrderNotFoundError("Available product not found.")
        return self._repository.add_confirmed_item(order, product, quantity, notes, actor.id)

    def update_item_status(self, actor: User, restaurant_id: int, item_id: int, status: OrderItemStatus) -> OrderItem:
        allowed_roles = {UserRole.ADMIN}
        if actor.role == UserRole.KITCHEN:
            allowed_roles.add(UserRole.KITCHEN)
        if actor.role == UserRole.BAR:
            allowed_roles.add(UserRole.BAR)
        self._authorize.execute(actor, restaurant_id, allowed_roles)
        item = self._repository.get_order_item(restaurant_id, item_id)
        if item is None:
            raise OrderNotFoundError("Order item not found.")
        if actor.role == UserRole.KITCHEN and item.station != Station.KITCHEN:
            raise OrderStateError("Kitchen users can update kitchen items only.")
        if actor.role == UserRole.BAR and item.station != Station.BAR:
            raise OrderStateError("Bar users can update bar items only.")
        return self._repository.update_item_status(restaurant_id, item_id, status)

    def close_order(self, actor: User, restaurant_id: int, order_id: int) -> Order:
        self._authorize.execute(actor, restaurant_id, {UserRole.WAITER, UserRole.ADMIN})
        order = self._repository.get_order(restaurant_id, order_id)
        if order is None:
            raise OrderNotFoundError("Order not found.")
        if order.status == OrderStatus.CLOSED:
            return order
        return self._repository.close_order(restaurant_id, order_id)

    def table_history(self, actor: User, restaurant_id: int, table_id: int) -> list[Order]:
        self._authorize.execute(actor, restaurant_id, {UserRole.WAITER, UserRole.ADMIN})
        table = self._repository.get_table(restaurant_id, table_id)
        if table is None:
            raise OrderNotFoundError("Table not found.")
        return self._repository.list_table_history(restaurant_id, table_id)

    def order_items(self, actor: User, restaurant_id: int, order_id: int) -> list[OrderItem]:
        self._authorize.execute(actor, restaurant_id, {UserRole.WAITER, UserRole.ADMIN, UserRole.KITCHEN, UserRole.BAR})
        if self._repository.get_order(restaurant_id, order_id) is None:
            raise OrderNotFoundError("Order not found.")
        return self._repository.list_order_items(restaurant_id, order_id)
