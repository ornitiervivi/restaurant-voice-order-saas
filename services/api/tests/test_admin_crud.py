"""Admin restaurant setup CRUD tests."""

import pytest

from src.application.admin.memory import InMemoryAdminRepository
from src.application.admin.use_cases import ManageRestaurantSetup
from src.application.auth.use_cases import AuthorizationError
from src.domain.admin import Station
from src.domain.user import User, UserRole
from src.infrastructure.security.tokens import HmacJwtTokenIssuer


class _Secret:
    def get_secret_value(self) -> str:
        return "local-development-change-me"


class _TokenSettings:
    jwt_secret = _Secret()
    access_token_ttl_minutes = 15
    refresh_token_ttl_minutes = 60


def _admin(restaurant_id: int = 1) -> User:
    return User(1, restaurant_id, "admin@example.test", "Admin", UserRole.ADMIN, "unused")


def test_admin_can_manage_users_tables_and_products() -> None:
    repository = InMemoryAdminRepository()
    setup = ManageRestaurantSetup(repository)
    actor = _admin()

    user = setup.create_user(actor, 1, " Waiter@Example.Test ", "Waiter", UserRole.WAITER, "hash")
    table = setup.create_table(actor, 1, "12")
    product = setup.create_product(actor, 1, "Coca Zero", Station.BAR, 700)

    assert user.email == "waiter@example.test"
    assert setup.update_user(actor, 1, user.id, "Senior Waiter", None).full_name == "Senior Waiter"
    assert setup.deactivate_user(actor, 1, user.id).is_active is False
    assert setup.update_table(actor, 1, table.id, "Mesa 12", False).is_active is False
    assert setup.update_product(actor, 1, product.id, "Coca-Cola Zero", Station.BAR, 800, False).is_available is False
    assert setup.list_users(actor, 1)
    assert setup.list_tables(actor, 1)[0].label == "Mesa 12"
    assert setup.list_products(actor, 1)[0].station == Station.BAR


def test_admin_crud_enforces_tenant_and_role_isolation() -> None:
    setup = ManageRestaurantSetup(InMemoryAdminRepository())
    waiter = User(2, 1, "waiter@example.test", "Waiter", UserRole.WAITER, "unused")
    other_tenant_admin = _admin(restaurant_id=2)

    with pytest.raises(AuthorizationError):
        setup.list_products(waiter, 1)

    with pytest.raises(AuthorizationError):
        setup.list_tables(other_tenant_admin, 1)


def test_admin_http_routes_require_admin_token_and_support_crud() -> None:
    pytest.importorskip("fastapi")
    TestClient = pytest.importorskip("fastapi.testclient").TestClient
    from src.main import create_app

    client = TestClient(create_app())
    token = HmacJwtTokenIssuer(_TokenSettings()).issue_access_token(_admin())
    headers = {"Authorization": f"Bearer {token}"}

    table_response = client.post("/restaurants/1/admin/tables", json={"label": "7"}, headers=headers)
    product_response = client.post(
        "/restaurants/1/admin/products",
        json={"name": "Picanha", "station": "kitchen", "price_cents": 5900},
        headers=headers,
    )
    user_response = client.post(
        "/restaurants/1/admin/users",
        json={"email": "kitchen@example.test", "full_name": "Kitchen", "role": "kitchen", "password": "valid-password"},
        headers=headers,
    )

    assert table_response.status_code == 201
    assert table_response.json()["label"] == "7"
    assert product_response.status_code == 201
    assert product_response.json()["station"] == "kitchen"
    assert user_response.status_code == 201
    assert user_response.json()["role"] == "kitchen"


def test_admin_http_routes_reject_cross_tenant_access() -> None:
    pytest.importorskip("fastapi")
    TestClient = pytest.importorskip("fastapi.testclient").TestClient
    from src.main import create_app

    client = TestClient(create_app())
    token = HmacJwtTokenIssuer(_TokenSettings()).issue_access_token(_admin(restaurant_id=2))

    response = client.get("/restaurants/1/admin/products", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin role required for this restaurant."}
