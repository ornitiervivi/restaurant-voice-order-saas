"""Realtime WebSocket tests."""

import pytest

from src.application.orders.memory import InMemoryOrderRepository
from src.application.orders.use_cases import ManageOrders
from src.application.realtime.memory import InMemoryRealtimeHub
from src.domain.admin import Station
from src.domain.order import OrderItemStatus
from src.domain.user import User, UserRole
from src.infrastructure.security.tokens import HmacJwtTokenIssuer


class _Secret:
    def get_secret_value(self) -> str:
        return "local-development-change-me"


class _TokenSettings:
    jwt_secret = _Secret()
    access_token_ttl_minutes = 15
    refresh_token_ttl_minutes = 60


def _user(role: UserRole = UserRole.WAITER, restaurant_id: int = 1, user_id: int = 2) -> User:
    return User(user_id, restaurant_id, f"{role}@example.test", role.value.title(), role, "unused")


def test_realtime_hub_publishes_only_after_confirmed_item_use_case() -> None:
    hub = InMemoryRealtimeHub()
    orders = ManageOrders(InMemoryOrderRepository(), hub)
    waiter = _user()

    assert hub.replay(1, station=Station.KITCHEN) == []

    order = orders.open_or_resume_order(waiter, 1, 1)
    item = orders.add_confirmed_item(waiter, 1, order.id, 1, 2, "ao ponto")
    events = hub.replay(1, item.station)

    assert len(events) == 1
    assert events[0].type == "confirmed_order_item_created"
    assert events[0].payload["id"] == item.id
    assert events[0].payload["status"] == "confirmed"


def test_realtime_hub_scopes_events_by_restaurant_station_and_replay_id() -> None:
    hub = InMemoryRealtimeHub()
    orders = ManageOrders(InMemoryOrderRepository(), hub)
    waiter = _user()
    order = orders.open_or_resume_order(waiter, 1, 1)
    kitchen_item = orders.add_confirmed_item(waiter, 1, order.id, 1, 1)
    bar_item = orders.add_confirmed_item(waiter, 1, order.id, 2, 1)

    assert [event.payload["id"] for event in hub.replay(1, kitchen_item.station)] == [kitchen_item.id]
    assert [event.payload["id"] for event in hub.replay(1, bar_item.station)] == [bar_item.id]
    assert hub.replay(2, kitchen_item.station) == []
    assert hub.replay(1, kitchen_item.station, last_event_id=1) == []


def test_status_updates_emit_station_scoped_realtime_event() -> None:
    hub = InMemoryRealtimeHub()
    orders = ManageOrders(InMemoryOrderRepository(), hub)
    waiter = _user()
    kitchen = _user(UserRole.KITCHEN, user_id=3)
    order = orders.open_or_resume_order(waiter, 1, 1)
    item = orders.add_confirmed_item(waiter, 1, order.id, 1, 1)

    updated = orders.update_item_status(kitchen, 1, item.id, OrderItemStatus.PREPARING)
    events = hub.replay(1, item.station)

    assert updated.status == OrderItemStatus.PREPARING
    assert [event.type for event in events] == ["confirmed_order_item_created", "order_item_status_changed"]
    assert events[-1].payload["status"] == "preparing"


def test_realtime_websocket_requires_auth_and_streams_confirmed_events() -> None:
    pytest.importorskip("fastapi")
    TestClient = pytest.importorskip("fastapi.testclient").TestClient
    from src.main import create_app

    client = TestClient(create_app())
    issuer = HmacJwtTokenIssuer(_TokenSettings())
    kitchen_token = issuer.issue_access_token(_user(UserRole.KITCHEN, user_id=3))
    waiter_token = issuer.issue_access_token(_user())
    waiter_headers = {"Authorization": f"Bearer {waiter_token}"}

    with pytest.raises(Exception):
        with client.websocket_connect("/ws/restaurants/1/stations/kitchen"):
            pass

    open_response = client.post("/restaurants/1/orders/tables/1/open", headers=waiter_headers)
    order_id = open_response.json()["id"]

    with client.websocket_connect(f"/ws/restaurants/1/stations/kitchen?token={kitchen_token}") as websocket:
        item_response = client.post(
            f"/restaurants/1/orders/{order_id}/confirmed-items",
            json={"product_id": 1, "quantity": 1},
            headers=waiter_headers,
        )
        assert item_response.status_code == 201
        message = websocket.receive_json()
        assert message["type"] == "confirmed_order_item_created"
        assert message["restaurant_id"] == 1
        assert message["station"] == "kitchen"
        assert message["payload"]["id"] == item_response.json()["id"]
