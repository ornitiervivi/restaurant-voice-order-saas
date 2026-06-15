"""Order lifecycle tests."""

import pytest

from src.application.auth.use_cases import AuthorizationError
from src.application.orders.memory import InMemoryOrderRepository
from src.application.orders.use_cases import ManageOrders, OrderStateError
from src.domain.order import OrderItemStatus, OrderStatus
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


def test_waiter_can_open_resume_add_confirmed_items_and_view_history() -> None:
    repository = InMemoryOrderRepository()
    orders = ManageOrders(repository)
    waiter = _user()

    opened = orders.open_or_resume_order(waiter, 1, 1)
    resumed = orders.open_or_resume_order(waiter, 1, 1)
    item = orders.add_confirmed_item(waiter, 1, opened.id, 1, 2, "ao ponto")

    assert resumed.id == opened.id
    assert item.status == OrderItemStatus.CONFIRMED
    assert item.product_name == "Picanha"
    assert item.quantity == 2
    assert orders.table_history(waiter, 1, 1) == [opened]
    assert orders.order_items(waiter, 1, opened.id) == [item]


def test_station_users_update_only_items_routed_to_their_station() -> None:
    orders = ManageOrders(InMemoryOrderRepository())
    waiter = _user()
    kitchen = _user(UserRole.KITCHEN, user_id=3)
    bar = _user(UserRole.BAR, user_id=4)
    order = orders.open_or_resume_order(waiter, 1, 1)
    kitchen_item = orders.add_confirmed_item(waiter, 1, order.id, 1, 1)
    bar_item = orders.add_confirmed_item(waiter, 1, order.id, 2, 1)

    updated = orders.update_item_status(kitchen, 1, kitchen_item.id, OrderItemStatus.PREPARING)
    assert updated.status == OrderItemStatus.PREPARING

    with pytest.raises(OrderStateError):
        orders.update_item_status(kitchen, 1, bar_item.id, OrderItemStatus.READY)

    assert orders.update_item_status(bar, 1, bar_item.id, OrderItemStatus.READY).status == OrderItemStatus.READY


def test_closed_orders_reject_new_items_without_reopen_flow() -> None:
    orders = ManageOrders(InMemoryOrderRepository())
    waiter = _user()
    order = orders.open_or_resume_order(waiter, 1, 1)

    closed = orders.close_order(waiter, 1, order.id)

    assert closed.status == OrderStatus.CLOSED
    with pytest.raises(OrderStateError):
        orders.add_confirmed_item(waiter, 1, order.id, 1, 1)


def test_order_lifecycle_enforces_tenant_and_role_isolation() -> None:
    orders = ManageOrders(InMemoryOrderRepository())
    admin_other_tenant = _user(UserRole.ADMIN, restaurant_id=2)
    kitchen = _user(UserRole.KITCHEN)

    with pytest.raises(AuthorizationError):
        orders.open_or_resume_order(kitchen, 1, 1)

    with pytest.raises(AuthorizationError):
        orders.table_history(admin_other_tenant, 1, 1)


def test_order_http_routes_support_lifecycle() -> None:
    pytest.importorskip("fastapi")
    TestClient = pytest.importorskip("fastapi.testclient").TestClient
    from src.main import create_app

    client = TestClient(create_app())
    waiter_token = HmacJwtTokenIssuer(_TokenSettings()).issue_access_token(_user())
    kitchen_token = HmacJwtTokenIssuer(_TokenSettings()).issue_access_token(_user(UserRole.KITCHEN, user_id=3))
    waiter_headers = {"Authorization": f"Bearer {waiter_token}"}
    kitchen_headers = {"Authorization": f"Bearer {kitchen_token}"}

    open_response = client.post("/restaurants/1/orders/tables/1/open", headers=waiter_headers)
    assert open_response.status_code == 201
    order_id = open_response.json()["id"]

    item_response = client.post(
        f"/restaurants/1/orders/{order_id}/confirmed-items",
        json={"product_id": 1, "quantity": 2, "notes": "ao ponto"},
        headers=waiter_headers,
    )
    assert item_response.status_code == 201
    assert item_response.json()["status"] == "confirmed"

    status_response = client.patch(
        f"/restaurants/1/orders/items/{item_response.json()['id']}/status",
        json={"status": "preparing"},
        headers=kitchen_headers,
    )
    assert status_response.status_code == 200
    assert status_response.json()["status"] == "preparing"

    close_response = client.post(f"/restaurants/1/orders/{order_id}/close", headers=waiter_headers)
    assert close_response.status_code == 200
    assert close_response.json()["status"] == "closed"

    rejected_response = client.post(
        f"/restaurants/1/orders/{order_id}/confirmed-items",
        json={"product_id": 1, "quantity": 1},
        headers=waiter_headers,
    )
    assert rejected_response.status_code == 409
