from fastapi import WebSocket

websocket_clients: list[WebSocket] = []


async def broadcast_limit_exceeded():
    message = {
        "limit_exceeded_real_time_alert": True,
    }
    print('messagefrmbroadcsar', message)
    for client in websocket_clients.copy():
        try:
            await client.send_json(message)
            print("Sent to client", client)
        except Exception:
            print("Send failed:")
            websocket_clients.remove(client)