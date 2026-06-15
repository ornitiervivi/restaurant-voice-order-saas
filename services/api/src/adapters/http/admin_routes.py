"""HTTP routes for admin restaurant setup CRUD."""

from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel, Field

from src.application.admin.memory import InMemoryAdminRepository
from src.application.admin.use_cases import AdminNotFoundError, ManageRestaurantSetup
from src.application.auth.use_cases import AuthorizationError
from src.domain.admin import Station
from src.domain.user import User, UserRole
from src.infrastructure.security.passwords import Pbkdf2PasswordHasher
from src.infrastructure.security.tokens import HmacJwtTokenIssuer, TokenVerificationError
from src.infrastructure.settings import get_settings

router = APIRouter(prefix="/restaurants/{restaurant_id}/admin", tags=["admin"])
_repository = InMemoryAdminRepository()


class RestaurantResponse(BaseModel):
    id: int
    name: str
    slug: str
    is_active: bool


class UpdateRestaurantRequest(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    slug: str = Field(min_length=1, max_length=80)


class UserResponse(BaseModel):
    id: int
    restaurant_id: int
    email: str
    full_name: str
    role: UserRole
    is_active: bool


class CreateUserRequest(BaseModel):
    email: str = Field(min_length=3, max_length=254)
    full_name: str = Field(min_length=1, max_length=160)
    role: UserRole
    password: str = Field(min_length=8, max_length=256)


class UpdateUserRequest(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=160)
    role: UserRole | None = None


class TableResponse(BaseModel):
    id: int
    restaurant_id: int
    label: str
    is_active: bool


class CreateTableRequest(BaseModel):
    label: str = Field(min_length=1, max_length=40)


class UpdateTableRequest(BaseModel):
    label: str | None = Field(default=None, min_length=1, max_length=40)
    is_active: bool | None = None


class ProductResponse(BaseModel):
    id: int
    restaurant_id: int
    name: str
    station: Station
    price_cents: int
    is_available: bool


class CreateProductRequest(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    station: Station
    price_cents: int = Field(ge=0)


class UpdateProductRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=160)
    station: Station | None = None
    price_cents: int | None = Field(default=None, ge=0)
    is_available: bool | None = None


def _current_user(authorization: Annotated[str | None, Header()] = None) -> User:
    if authorization is None or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token.")
    token = authorization.split(" ", 1)[1]
    try:
        claims = HmacJwtTokenIssuer(get_settings()).verify_access_token(token)
        return User(
            id=int(claims["sub"]),
            restaurant_id=int(claims["restaurant_id"]),
            email=str(claims.get("email", "")),
            full_name="Authenticated User",
            role=UserRole(str(claims["role"])),
            password_hash="",
        )
    except (KeyError, ValueError, TokenVerificationError) as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid bearer token.") from exc


def _use_case() -> ManageRestaurantSetup:
    return ManageRestaurantSetup(_repository)


def _translate_errors(func):
    try:
        return func()
    except AuthorizationError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin role required for this restaurant.") from exc
    except AdminNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/profile", response_model=RestaurantResponse)
def get_profile(restaurant_id: int, actor: Annotated[User, Depends(_current_user)]) -> object:
    return _translate_errors(lambda: _use_case().get_restaurant(actor, restaurant_id))


@router.put("/profile", response_model=RestaurantResponse)
def update_profile(restaurant_id: int, payload: UpdateRestaurantRequest, actor: Annotated[User, Depends(_current_user)]) -> object:
    return _translate_errors(lambda: _use_case().update_restaurant(actor, restaurant_id, payload.name, payload.slug))


@router.get("/users", response_model=list[UserResponse])
def list_users(restaurant_id: int, actor: Annotated[User, Depends(_current_user)]) -> object:
    return _translate_errors(lambda: _use_case().list_users(actor, restaurant_id))


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(restaurant_id: int, payload: CreateUserRequest, actor: Annotated[User, Depends(_current_user)]) -> object:
    password_hash = Pbkdf2PasswordHasher().hash(payload.password)
    return _translate_errors(lambda: _use_case().create_user(actor, restaurant_id, payload.email, payload.full_name, payload.role, password_hash))


@router.patch("/users/{user_id}", response_model=UserResponse)
def update_user(restaurant_id: int, user_id: int, payload: UpdateUserRequest, actor: Annotated[User, Depends(_current_user)]) -> object:
    return _translate_errors(lambda: _use_case().update_user(actor, restaurant_id, user_id, payload.full_name, payload.role))


@router.delete("/users/{user_id}", response_model=UserResponse)
def deactivate_user(restaurant_id: int, user_id: int, actor: Annotated[User, Depends(_current_user)]) -> object:
    return _translate_errors(lambda: _use_case().deactivate_user(actor, restaurant_id, user_id))


@router.get("/tables", response_model=list[TableResponse])
def list_tables(restaurant_id: int, actor: Annotated[User, Depends(_current_user)]) -> object:
    return _translate_errors(lambda: _use_case().list_tables(actor, restaurant_id))


@router.post("/tables", response_model=TableResponse, status_code=status.HTTP_201_CREATED)
def create_table(restaurant_id: int, payload: CreateTableRequest, actor: Annotated[User, Depends(_current_user)]) -> object:
    return _translate_errors(lambda: _use_case().create_table(actor, restaurant_id, payload.label))


@router.patch("/tables/{table_id}", response_model=TableResponse)
def update_table(restaurant_id: int, table_id: int, payload: UpdateTableRequest, actor: Annotated[User, Depends(_current_user)]) -> object:
    return _translate_errors(lambda: _use_case().update_table(actor, restaurant_id, table_id, payload.label, payload.is_active))


@router.get("/products", response_model=list[ProductResponse])
def list_products(restaurant_id: int, actor: Annotated[User, Depends(_current_user)]) -> object:
    return _translate_errors(lambda: _use_case().list_products(actor, restaurant_id))


@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(restaurant_id: int, payload: CreateProductRequest, actor: Annotated[User, Depends(_current_user)]) -> object:
    return _translate_errors(lambda: _use_case().create_product(actor, restaurant_id, payload.name, payload.station, payload.price_cents))


@router.patch("/products/{product_id}", response_model=ProductResponse)
def update_product(restaurant_id: int, product_id: int, payload: UpdateProductRequest, actor: Annotated[User, Depends(_current_user)]) -> object:
    return _translate_errors(lambda: _use_case().update_product(actor, restaurant_id, product_id, payload.name, payload.station, payload.price_cents, payload.is_available))
