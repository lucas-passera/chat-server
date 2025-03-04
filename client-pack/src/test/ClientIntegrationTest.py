import pytest
import asyncio
import websockets

WS_URL = "ws://localhost:8081/chat" 

@pytest.mark.asyncio
async def test_websocket_connection():
    async with websockets.connect(WS_URL) as ws:
        assert ws.open 