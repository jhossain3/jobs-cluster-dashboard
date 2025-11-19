from fastapi import APIRouter, WebSocket
from ..repository.fia_compliance_repository import FiaComplianceRepository
from backend.websocket_manager import websocket_clients  # import the list

router = APIRouter()
fia_compliance_repo = FiaComplianceRepository()

#websocket endpoint for listening for FIA limit updates
@router.websocket("/ws/limit")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_clients.append(websocket)

    await websocket.send_json({"hello": "sdf"})

    try:
        while True:
            # Receive any type of message (text, binary, ping, pong)
            await websocket.receive()
    except Exception:
        print("Client disconnected")
    finally:
        if websocket in websocket_clients:
            websocket_clients.remove(websocket)

# route for pulling current FIA compliance status
@router.get("/currentstatus")
async def get_current_status():
    return await fia_compliance_repo.get_fia_compliance_window()
