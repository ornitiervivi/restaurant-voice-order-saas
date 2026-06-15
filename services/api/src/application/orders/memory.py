"""In-memory order repository for tests and local demo routes."""

from dataclasses import replace

from src.application.orders.use_cases import OrderNotFoundError
from src.domain.admin import Product, RestaurantTable, Station
from src.domain.order import Order, OrderItem, OrderItemStatus, OrderStatus


class InMemoryOrderRepository:
    """Tenant-aware in-memory order repository."""

    def __init__(self) -> None:
        self.tables: dict[int, list[RestaurantTable]] = {1: [RestaurantTable(1, 1, "12"), RestaurantTable(2, 1, "7")]}
        self.products: dict[int, list[Product]] = {
            1: [Product(1, 1, "Picanha", Station.KITCHEN, 5900), Product(2, 1, "Coca Zero", Station.BAR, 700)]
        }
        self.orders: dict[int, list[Order]] = {1: []}
        self.items: dict[int, list[OrderItem]] = {1: []}
        self._next_order_id = 1
        self._next_item_id = 1

    def get_table(self, restaurant_id: int, table_id: int) -> RestaurantTable | None:
        return next((table for table in self.tables.get(restaurant_id, []) if table.id == table_id), None)

    def get_product(self, restaurant_id: int, product_id: int) -> Product | None:
        return next((product for product in self.products.get(restaurant_id, []) if product.id == product_id), None)

    def get_open_order_for_table(self, restaurant_id: int, table_id: int) -> Order | None:
        return next((order for order in self.orders.get(restaurant_id, []) if order.table_id == table_id and order.status == OrderStatus.OPEN), None)

    def create_order(self, restaurant_id: int, table_id: int, opened_by_user_id: int) -> Order:
        order = Order(self._next_order_id, restaurant_id, table_id, opened_by_user_id)
        self._next_order_id += 1
        self.orders.setdefault(restaurant_id, []).append(order)
        return order

    def get_order(self, restaurant_id: int, order_id: int) -> Order | None:
        return next((order for order in self.orders.get(restaurant_id, []) if order.id == order_id), None)

    def list_order_items(self, restaurant_id: int, order_id: int) -> list[OrderItem]:
        return [item for item in self.items.get(restaurant_id, []) if item.order_id == order_id]

    def get_order_item(self, restaurant_id: int, item_id: int) -> OrderItem | None:
        return next((item for item in self.items.get(restaurant_id, []) if item.id == item_id), None)

    def add_confirmed_item(self, order: Order, product: Product, quantity: int, notes: str | None, confirmed_by_user_id: int) -> OrderItem:
        item = OrderItem(
            self._next_item_id,
            order.restaurant_id,
            order.id,
            product.id,
            product.name,
            product.station,
            quantity,
            notes,
            confirmed_by_user_id,
        )
        self._next_item_id += 1
        self.items.setdefault(order.restaurant_id, []).append(item)
        return item

    def update_item_status(self, restaurant_id: int, item_id: int, status: OrderItemStatus) -> OrderItem:
        items = self.items.get(restaurant_id, [])
        for index, item in enumerate(items):
            if item.id == item_id:
                updated = replace(item, status=status)
                items[index] = updated
                return updated
        raise OrderNotFoundError("Order item not found.")

    def close_order(self, restaurant_id: int, order_id: int) -> Order:
        orders = self.orders.get(restaurant_id, [])
        for index, order in enumerate(orders):
            if order.id == order_id:
                updated = replace(order, status=OrderStatus.CLOSED)
                orders[index] = updated
                return updated
        raise OrderNotFoundError("Order not found.")

    def list_table_history(self, restaurant_id: int, table_id: int) -> list[Order]:
        return [order for order in self.orders.get(restaurant_id, []) if order.table_id == table_id]
