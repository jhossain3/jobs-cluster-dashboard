# domain/models/job_summary.py

class JobSummary:
    def __init__(self, totals_by_type: dict, overall_total: float):
        self.totals_by_type = totals_by_type
        self.overall_total = overall_total

    def to_dict(self):
        return {
            "totals_by_type": self.totals_by_type,
            "overall_total": self.overall_total,
        }
