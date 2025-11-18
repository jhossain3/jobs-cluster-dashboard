from fastapi import APIRouter, WebSocket
from ..repository.fia_compliance_repository import FiaComplianceRepository
from backend.websocket_manager import websocket_clients  # import the list

router = APIRouter()
fia_compliance_repo = FiaComplianceRepository()


@router.websocket("/ws/limit")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()
    websocket_clients.append(websocket)
    await websocket.send_json({"hello": "sdf"})  # test push

    try:
        while True:
            # keep alive (client can send pings)
            await websocket.receive_text()
    except Exception:
        websocket_clients.remove(websocket)


@router.get("/currentstatus")
async def get_current_status():
    return await fia_compliance_repo.get_fia_compliance_window()
