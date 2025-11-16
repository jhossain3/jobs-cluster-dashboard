# application/job_service.py
from model.job_summary import JobSummary

class JobService:
    def __init__(self, repository):
        self.repository = repository

    def get_summary(self):
        raw = self.repository.get_auh_summary()
        totals_by_type = {r["_id"]: r["total_auh"] for r in raw}
        overall_total = sum(totals_by_type.values())
        return JobSummary(totals_by_type, overall_total)
