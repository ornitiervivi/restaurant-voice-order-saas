"""Realtime event contracts and in-memory delivery hub."""

from dataclasses import asdict, dataclass
from typing import Protocol

from src.domain.admin import Station
from src.domain.order import OrderItem, OrderItemStatus


@dataclass(frozen=True)
class RealtimeEvent:
    """Tenant-scoped event delivered to realtime clients."""

    id: int
    restaurant_id: int
    station: Station
    type: str
    payload: dict[str, object]

    def to_message(self) -> dict[str, object]:
        return {
            "id": self.id,
            "restaurant_id": self.restaurant_id,
            "station": self.station.value,
            "type": self.type,
            "payload": self.payload,
        }


class RealtimeEventPublisher(Protocol):
    """Port for publishing confirmed order lifecycle events."""

    def publish_confirmed_order_item(self, item: OrderItem) -> RealtimeEvent: ...
    def publish_order_item_status_changed(self, item: OrderItem) -> RealtimeEvent: ...


def order_item_payload(item: OrderItem) -> dict[str, object]:
    """Return a JSON-safe representation of a confirmed order item."""

    data = asdict(item)
    data["station"] = item.station.value
    data["status"] = item.status.value
    return data
