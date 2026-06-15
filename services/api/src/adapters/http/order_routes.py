"""HTTP routes for order lifecycle operations."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from src.adapters.http.admin_routes import _current_user
from src.application.auth.use_cases import AuthorizationError
from src.application.orders.memory import InMemoryOrderRepository
from src.application.orders.use_cases import ManageOrders, OrderNotFoundError, OrderStateError
from src.domain.admin import Station
from src.domain.order import OrderItemStatus, OrderStatus
from src.domain.user import User
from src.infrastructure.realtime import realtime_hub

router = APIRouter(prefix="/restaurants/{restaurant_id}/orders", tags=["orders"])
_repository = InMemoryOrderRepository()


class OrderResponse(BaseModel):
    id: int
    restaurant_id: int
    table_id: int
    opened_by_user_id: int
    status: OrderStatus


class OrderItemResponse(BaseModel):
    id: int
    restaurant_id: int
    order_id: int
    product_id: int
    product_name: str
    station: Station
    quantity: int
    notes: str | None
    confirmed_by_user_id: int
    status: OrderItemStatus


class AddConfirmedItemRequest(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    notes: str | None = Field(default=None, max_length=500)


class UpdateItemStatusRequest(BaseModel):
    status: OrderItemStatus


def _use_case() -> ManageOrders:
    return ManageOrders(_repository, realtime_hub)


def _translate_errors(func):
    try:
        return func()
    except AuthorizationError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Role not allowed for this restaurant order operation.") from exc
    except OrderNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except OrderStateError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.post("/tables/{table_id}/open", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def open_or_resume_order(restaurant_id: int, table_id: int, actor: Annotated[User, Depends(_current_user)]) -> object:
    return _translate_errors(lambda: _use_case().open_or_resume_order(actor, restaurant_id, table_id))


@router.get("/tables/{table_id}/history", response_model=list[OrderResponse])
def table_history(restaurant_id: int, table_id: int, actor: Annotated[User, Depends(_current_user)]) -> object:
    return _translate_errors(lambda: _use_case().table_history(actor, restaurant_id, table_id))


@router.get("/{order_id}/items", response_model=list[OrderItemResponse])
def order_items(restaurant_id: int, order_id: int, actor: Annotated[User, Depends(_current_user)]) -> object:
    return _translate_errors(lambda: _use_case().order_items(actor, restaurant_id, order_id))


@router.post("/{order_id}/confirmed-items", response_model=OrderItemResponse, status_code=status.HTTP_201_CREATED)
def add_confirmed_item(restaurant_id: int, order_id: int, payload: AddConfirmedItemRequest, actor: Annotated[User, Depends(_current_user)]) -> object:
    return _translate_errors(lambda: _use_case().add_confirmed_item(actor, restaurant_id, order_id, payload.product_id, payload.quantity, payload.notes))


@router.patch("/items/{item_id}/status", response_model=OrderItemResponse)
def update_item_status(restaurant_id: int, item_id: int, payload: UpdateItemStatusRequest, actor: Annotated[User, Depends(_current_user)]) -> object:
    return _translate_errors(lambda: _use_case().update_item_status(actor, restaurant_id, item_id, payload.status))


@router.post("/{order_id}/close", response_model=OrderResponse)
def close_order(restaurant_id: int, order_id: int, actor: Annotated[User, Depends(_current_user)]) -> object:
    return _translate_errors(lambda: _use_case().close_order(actor, restaurant_id, order_id))
