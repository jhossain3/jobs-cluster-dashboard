from ..db.mongo import fia_compliance_collection
from ..websocket_manager import broadcast_limit_exceeded
from ..repository.fia_compliance_repository import FiaComplianceRepository
from datetime import datetime, timezone

fia_compliance_repo = FiaComplianceRepository()

#asss a listener to watch for limit_exceeded changes and broadcast via websocket
async def watch_limit_exceeded():

    now = datetime.now(timezone.utc)
    fia_window = await fia_compliance_repo.get_fia_window(now)

    pipeline = [
        {
            "$match": {
                "operationType": "update",
                "documentKey._id": fia_window["_id"],
                "updateDescription.updatedFields.limit_exceeded": 
                    {"$exists": True},
            }
        }
    ]

    async with fia_compliance_collection.watch(pipeline) as stream:

        async for change in stream:
            print("Change event:", change)  
            
            new_value = (
                change["updateDescription"]["updatedFields"]["limit_exceeded"]
            )
            print("limit_exceeded changed:", new_value)

            if new_value:
                await broadcast_limit_exceeded()
