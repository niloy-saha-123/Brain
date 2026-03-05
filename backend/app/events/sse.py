"""SSE endpoint for streaming run events."""
from __future__ import annotations

import asyncio
import json
from typing import AsyncIterator

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from app.events.bus import event_bus
from app.core.config import Settings, get_settings

router = APIRouter()


async def _format_sse(event: dict) -> str:
    return f"event: {event.get('type', 'message')}\ndata: {json.dumps(event)}\n\n"


@router.get("/runs/{run_id}/events", summary="Stream events for a run", response_model=None)
async def stream_run_events(run_id: str, _: Settings = Depends(get_settings)) -> StreamingResponse:
    if not run_id:
        raise HTTPException(status_code=400, detail="run_id required")

    async def event_generator() -> AsyncIterator[str]:
        event_iter = event_bus.stream(run_id)
        try:
            while True:
                event_task = asyncio.create_task(event_iter.__anext__())
                heartbeat = asyncio.create_task(asyncio.sleep(15.0))
                done, pending = await asyncio.wait(
                    {event_task, heartbeat}, return_when=asyncio.FIRST_COMPLETED
                )
                if event_task in done:
                    for task in pending:
                        task.cancel()
                    try:
                        event = event_task.result()
                    except StopAsyncIteration:
                        break
                    yield await _format_sse(event)
                else:
                    # heartbeat fired
                    yield "event: heartbeat\ndata: {}\n\n"
                    event_task.cancel()
        finally:
            if hasattr(event_iter, "aclose"):
                await event_iter.aclose()  # type: ignore[attr-defined]

    return StreamingResponse(event_generator(), media_type="text/event-stream")
