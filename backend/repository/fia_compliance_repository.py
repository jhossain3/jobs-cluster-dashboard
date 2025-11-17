from ..db.mongo import fia_compliance_collection, jobs_collection
from datetime import datetime


class FiaComplianceRepository:
    def __init__(self):
        self.jobs_collection = jobs_collection
        self.fia_compliance_collection = fia_compliance_collection
        
    def get_fia_window(self, start_time: datetime):
        fia_window = self.fia_compliance_collection.find_one({
            "start_date": {"$lte": start_time},
            "end_date": {"$gt": start_time}
        })
        return fia_window

    def increment_total(self, start_time, auh):
        fia_window = self.get_fia_window(start_time)

        if fia_window:
            new_total = fia_window["current_auh_count"] + auh
            self.fia_compliance_collection.update_one(
                {"_id": fia_window["_id"]},
                {
                    "$inc": {"current_auh_count": auh},
                    "$set": {"limit_exceeded": new_total > fia_window["limit"]}
                }
            )