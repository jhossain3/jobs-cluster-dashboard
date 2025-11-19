# these models are unused but kept for reference as they are important to check the data before sending to the frontend
class JobSummary:
    def __init__(self, totals_by_type: dict, overall_total: float):
        self.totals_by_type = totals_by_type
        self.overall_total = overall_total

    def to_dict(self):
        return {
            "totals_by_type": self.totals_by_type,
            "overall_total": self.overall_total,
        }
