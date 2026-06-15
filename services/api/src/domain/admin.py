"""Restaurant setup domain models."""

from dataclasses import dataclass
from enum import StrEnum


class Station(StrEnum):
    """Stations that receive confirmed product items."""

    KITCHEN = "kitchen"
    BAR = "bar"


@dataclass(frozen=True)
class RestaurantProfile:
    """Restaurant profile visible to tenant admins."""

    id: int
    name: str
    slug: str
    is_active: bool = True


@dataclass(frozen=True)
class RestaurantTable:
    """Physical table managed by a restaurant."""

    id: int
    restaurant_id: int
    label: str
    is_active: bool = True


@dataclass(frozen=True)
class Product:
    """Menu product routed to a preparation station."""

    id: int
    restaurant_id: int
    name: str
    station: Station
    price_cents: int
    is_available: bool = True
