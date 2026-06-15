"""Realtime infrastructure wiring for the local MVP."""

from src.application.realtime.memory import InMemoryRealtimeHub

realtime_hub = InMemoryRealtimeHub()
