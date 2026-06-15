"""In-memory realtime hub for local FastAPI WebSocket delivery."""

import asyncio
from collections import defaultdict

from src.application.realtime.events import RealtimeEvent, order_item_payload
from src.domain.admin import Station
from src.domain.order import OrderItem


class InMemoryRealtimeHub:
    """Restaurant/station-scoped event publisher with replay support.

    This MVP implementation keeps events in process. It defines the port behavior
    expected by use cases and can be replaced by Redis/pub-sub without changing
    order lifecycle rules.
    """

    def __init__(self) -> None:
        self._next_event_id = 1
        self._events: dict[tuple[int, Station], list[RealtimeEvent]] = defaultdict(list)
        self._subscribers: dict[tuple[int, Station], set[asyncio.Queue[RealtimeEvent]]] = defaultdict(set)

    def publish_confirmed_order_item(self, item: OrderItem) -> RealtimeEvent:
        return self._publish(item.restaurant_id, item.station, "confirmed_order_item_created", order_item_payload(item))

    def publish_order_item_status_changed(self, item: OrderItem) -> RealtimeEvent:
        return self._publish(item.restaurant_id, item.station, "order_item_status_changed", order_item_payload(item))

    def replay(self, restaurant_id: int, station: Station, last_event_id: int = 0) -> list[RealtimeEvent]:
        return [event for event in self._events.get((restaurant_id, station), []) if event.id > last_event_id]

    def subscribe(self, restaurant_id: int, station: Station) -> asyncio.Queue[RealtimeEvent]:
        queue: asyncio.Queue[RealtimeEvent] = asyncio.Queue()
        self._subscribers[(restaurant_id, station)].add(queue)
        return queue

    def unsubscribe(self, restaurant_id: int, station: Station, queue: asyncio.Queue[RealtimeEvent]) -> None:
        self._subscribers[(restaurant_id, station)].discard(queue)

    def _publish(self, restaurant_id: int, station: Station, event_type: str, payload: dict[str, object]) -> RealtimeEvent:
        event = RealtimeEvent(self._next_event_id, restaurant_id, station, event_type, payload)
        self._next_event_id += 1
        key = (restaurant_id, station)
        self._events[key].append(event)
        for queue in list(self._subscribers.get(key, set())):
            queue.put_nowait(event)
        return event
