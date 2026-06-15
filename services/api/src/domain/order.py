"""Order lifecycle domain models and invariants."""

from dataclasses import dataclass
from enum import StrEnum

from src.domain.admin import Station


class OrderStatus(StrEnum):
    """Supported order/tab lifecycle states."""

    OPEN = "open"
    CLOSED = "closed"


class OrderItemStatus(StrEnum):
    """Preparation statuses for human-confirmed order items."""

    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELED = "canceled"


@dataclass(frozen=True)
class Order:
    """Restaurant table order/tab."""

    id: int
    restaurant_id: int
    table_id: int
    opened_by_user_id: int
    status: OrderStatus = OrderStatus.OPEN

    def can_accept_items(self) -> bool:
        """Return whether new confirmed items can be inserted."""

        return self.status == OrderStatus.OPEN


@dataclass(frozen=True)
class OrderItem:
    """Human-confirmed order line routed to a preparation station."""

    id: int
    restaurant_id: int
    order_id: int
    product_id: int
    product_name: str
    station: Station
    quantity: int
    notes: str | None
    confirmed_by_user_id: int
    status: OrderItemStatus = OrderItemStatus.CONFIRMED
