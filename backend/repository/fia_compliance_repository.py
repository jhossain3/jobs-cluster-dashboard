# from ..main import websocket_clients  # import from wherever it's defined
from ..db.mongo import fia_compliance_collection, jobs_collection
from datetime import datetime, timezone
import asyncio


class FiaComplianceRepository:
    def __init__(self):
        self.jobs_collection = jobs_collection
        self.fia_compliance_collection = fia_compliance_collection
        # self.websocket_clients = websocket_clients
    
    def is_limit_exceeded(self):
        now = datetime.now(timezone.utc)
        fia_window = fia_compliance_collection.find_one({
        "start_date": {"$lte": now},
        "end_date": {"$gte": now}
    })
        if fia_window:
            return {
                "period": fia_window["period_cycle"],
                "start_date": fia_window["start_date"],
                "end_date": fia_window["end_date"],
                "current_auh": fia_window["current_auh_count"],
                "limit": fia_window["limit"],
                "limit_exceeded": fia_window["limit_exceeded"]
            }
        return {"message": "No active compliance window"}

    def get_fia_window(self, start_time: datetime):
        fia_window = self.fia_compliance_collection.find_one({
            "start_date": {"$lte": start_time},
            "end_date": {"$gt": start_time}
        })
        return fia_window
    
    # async def notify_limit_exceeded(self, fia_window, new_total):
    #     message = {
    #         "period": fia_window["period_cycle"],
    #         "current_auh": new_total,
    #         "limit": fia_window["limit"]
    #     }
    #     for client in self.websocket_clients:
    #         try:
    #             await client.send_json(message)
    #         except Exception as e:
    #             handle_error(e)  
    #             self.websocket_clients.remove(client)

    def increment_total(self, start_time, auh):
        fia_window = self.get_fia_window(start_time)
    
        if fia_window:
            new_total = fia_window["current_auh_count"] + auh
            limit_exceeded = new_total > fia_window["limit"]

            self.fia_compliance_collection.update_one(
                {"_id": fia_window["_id"]},
                {
                    "$inc": {"current_auh_count": auh},
                    "$set": {"limit_exceeded": limit_exceeded}
                }
            )
            
            # if limit_exceeded:
            #     asyncio.create_task(self.notify_limit_exceeded(fia_window, new_total))
            
    