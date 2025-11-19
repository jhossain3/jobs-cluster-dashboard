from fastapi import WebSocket

websocket_clients: list[WebSocket] = []

# have one single source of websocket clients shared between modules
# when a new client connects, add to this list
# when broadcasting, iterate over this list and send messages

async def broadcast_limit_exceeded():
    message = {
        "limit_exceeded_real_time_alert": True,
    }
    print('message from broadcaster', message)
    for client in websocket_clients.copy():
        try:
            await client.send_json(message)
            print("Sent to client", client)
        except Exception:
            print("Send failed:")
            websocket_clients.remove(client)
