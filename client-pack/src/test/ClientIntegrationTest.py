import json
import pytest
import asyncio
import websockets

WS_URL = "ws://localhost:8081/chat" 


@pytest.mark.asyncio
async def test_check_websocket_connection():
    async with websockets.connect(WS_URL) as ws:
        assert ws.open #Si el servidor está funcionando y acepta conexiones, la prueba pasa.

@pytest.mark.asyncio
async def test_send_and_receive_message():
    async with websockets.connect(WS_URL) as ws:
        #Send message simulation
        message = {"user_id": 1, "username": "testuser", "content": "Hi server"}
        await ws.send(json.dumps(message))
        #Waiting for a response
        response = await ws.recv()
        response_data = json.loads(response)

        assert "content" in response_data
        assert response_data["content"] == "Hi server"