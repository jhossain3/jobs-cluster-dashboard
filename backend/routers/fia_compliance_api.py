from fastapi import APIRouter, WebSocket
from ..repository.fia_compliance_repository import FiaComplianceRepository
from datetime import datetime, timezone

router = APIRouter()
fia_compliance_repo = FiaComplianceRepository()



# Keep a global list of connected clients
# websocket_clients = []

# @router.websocket("/ws/limit")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     websocket_clients.append(websocket)

#     fia_window = fia_compliance_collection.find_one({
#         "start_date": {"$lte": now},
#         "end_date": {"$gte": now}
#     })

#     if fia_window and fia_window.get("limit_exceeded"):
#         await websocket.send_json({
#             "period": fia_window["period_cycle"],
#             "current_auh": fia_window["current_auh_count"],
#             "limit": fia_window["limit"]
#         })

#     try:
#         while True:
#             await websocket.receive_text()  # keep alive
#     except:
#         websocket_clients.remove(websocket)
        
        
@router.get("/currentstatus")
def get_current_status():
    return fia_compliance_repo.is_limit_exceeded()
    
    