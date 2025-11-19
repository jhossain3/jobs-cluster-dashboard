# from ..main import websocket_clients  # import from wherever it's defined
from ..db.mongo import fia_compliance_collection, jobs_collection
from datetime import datetime, timezone


class FiaComplianceRepository:
    def __init__(self):
        self.jobs_collection = jobs_collection
        self.fia_compliance_collection = fia_compliance_collection

    # Get the current FIA compliance window for the current time
    async def get_fia_compliance_window(self):
        now = datetime.now(timezone.utc)
        fia_window = await self.get_fia_window(now)
        
        if fia_window:
            return {
                "start_date": fia_window["start_date"],
                "end_date": fia_window["end_date"],
                "current_auh": fia_window["current_auh_count"],
                "limit": fia_window["limit"],
                "limit_exceeded": fia_window["limit_exceeded"],
            }
        return {"message": "No active compliance window"}

    #get the FIA window for a specific date
    async def get_fia_window(self, start_time: datetime):
        fia_window = await self.fia_compliance_collection.find_one(
            {"start_date": {"$lte": start_time}, "end_date": 
                {"$gt": start_time}}
        )
        return fia_window

    # Increment the total AUH for the FIA compliance window that includes a given a date
    async def increment_total(self, start_time, auh):
        fia_window = await self.get_fia_window(start_time)

        if fia_window:
            new_total = fia_window["current_auh_count"] + auh
            limit_exceeded = new_total > fia_window["limit"]

            await self.fia_compliance_collection.update_one(
                {"_id": fia_window["_id"]},
                {
                    "$inc": {"current_auh_count": auh},
                    "$set": {"limit_exceeded": limit_exceeded},
                },
            )
