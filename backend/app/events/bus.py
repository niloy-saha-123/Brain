"""In-process event bus for streaming run events via SSE."""
from __future__ import annotations

import asyncio
from collections import defaultdict
from typing import Any, AsyncIterator, DefaultDict, Dict, List

EventPayload = Dict[str, Any]


class EventBus:
    def __init__(self) -> None:
        self._subscribers: DefaultDict[str, List[asyncio.Queue[EventPayload]]] = defaultdict(list)
        self._lock = asyncio.Lock()

    async def publish(self, event: EventPayload) -> None:
        run_id = event.get("run_id")
        if not run_id:
            return
        queues = list(self._subscribers.get(run_id, []))
        for queue in queues:
            try:
                queue.put_nowait(event)
            except asyncio.QueueFull:
                # drop to avoid blocking
                continue

    async def stream(self, run_id: str) -> AsyncIterator[EventPayload]:
        queue: asyncio.Queue[EventPayload] = asyncio.Queue(maxsize=100)
        async with self._lock:
            self._subscribers[run_id].append(queue)
        try:
            while True:
                event = await queue.get()
                yield event
        finally:
            async with self._lock:
                if queue in self._subscribers.get(run_id, []):
                    self._subscribers[run_id].remove(queue)


event_bus = EventBus()
