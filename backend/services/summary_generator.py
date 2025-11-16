from db.mongo import jobs_collection
from collections import defaultdict


class SummaryGenerator:
    @staticmethod
    def get_summary():
        jobs = jobs_collection.find({})  

        grouped = defaultdict(float)
        overall = 0.0

        for job in jobs:
            job_type = job.get("type")
            auh = job.get("calculated_auh", 0.0)
            if job_type:
                grouped[job_type] += auh
            overall += auh

        return {
            "per_type": dict(grouped),
            "overall": overall
        }
