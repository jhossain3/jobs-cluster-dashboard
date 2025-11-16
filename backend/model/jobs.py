# domain/job.py
from typing import Optional
from datetime import datetime
from services.auh_calculator import AUHCalculator


class Job:
    def __init__(self, job_id: int, job_type: str, event: str, start_time: datetime):
        self.job_id = job_id
        self.type = job_type
        self.event = event
        self.status = "running"
        self.start_time = start_time
        self.end_time: Optional[datetime] = None
        self.duration = None
        self.calculated_auh = 0.0 


    def process(self):
        """Business rule: only calculate AUH if event=completed and type=solve."""
        if self.event == "completed" and self.type == "solve" and 
        self.duration:
        self.calculated_auh = AUHCalculator.calculate(self.type, self.duration, self.event)
        else: self.calculated_auh = 0.0
        return 

    def to_dict(self):
        """Convert to a plain dict for persistence (MongoDB)."""
        return {
            "job_id": self.job_id,
            "type": self.type,
            "status": self.status,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": self.duration,
            "calculated_auh": self.calculated_auh(),
        }
