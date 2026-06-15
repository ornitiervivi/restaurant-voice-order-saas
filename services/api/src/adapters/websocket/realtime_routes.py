"""WebSocket routes for restaurant station realtime events."""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status

from src.application.auth.use_cases import AuthorizationError, AuthorizeRestaurantRole
from src.domain.admin import Station
from src.domain.user import User, UserRole
from src.infrastructure.security.tokens import HmacJwtTokenIssuer, TokenVerificationError
from src.infrastructure.realtime import realtime_hub
from src.infrastructure.settings import get_settings

router = APIRouter(tags=["realtime"])


def _user_from_token(token: str) -> User:
    claims = HmacJwtTokenIssuer(get_settings()).verify_access_token(token)
    return User(
        id=int(claims["sub"]),
        restaurant_id=int(claims["restaurant_id"]),
        email=str(claims.get("email", "")),
        full_name="Authenticated User",
        role=UserRole(str(claims["role"])),
        password_hash="",
    )


def _authorize_station(actor: User, restaurant_id: int, station: Station) -> None:
    allowed_roles = {UserRole.ADMIN}
    if station == Station.KITCHEN:
        allowed_roles.add(UserRole.KITCHEN)
    if station == Station.BAR:
        allowed_roles.add(UserRole.BAR)
    AuthorizeRestaurantRole().execute(actor, restaurant_id, allowed_roles)


@router.websocket("/ws/restaurants/{restaurant_id}/stations/{station}")
async def station_events(websocket: WebSocket, restaurant_id: int, station: Station, token: str | None = None, last_event_id: int = 0) -> None:
    """Stream confirmed station events after bearer-equivalent query auth."""

    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    try:
        actor = _user_from_token(token)
        _authorize_station(actor, restaurant_id, station)
    except (AuthorizationError, KeyError, ValueError, TokenVerificationError):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()
    for event in realtime_hub.replay(restaurant_id, station, last_event_id):
        await websocket.send_json(event.to_message())

    queue = realtime_hub.subscribe(restaurant_id, station)
    try:
        while True:
            event = await queue.get()
            await websocket.send_json(event.to_message())
    except WebSocketDisconnect:
        pass
    finally:
        realtime_hub.unsubscribe(restaurant_id, station, queue)
