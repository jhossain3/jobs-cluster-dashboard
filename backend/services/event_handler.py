# services/event_service.py
from datetime import datetime
from ..repository.job_repository import JobRepository
from ..repository.fia_compliance_repository import FiaComplianceRepository
from .auh_calculator import AUHCalculator


class EventService:
    def __init__(self):
        self.repo = JobRepository()
        self.fia_compliance_repository = FiaComplianceRepository()

    async def handle_event(self, job):
        if job["event"] == "start":
            job_doc = {
                "job_id": job["id"],
                "type": job["type"],
                "status": "running",
                "start_time": datetime.fromisoformat(job["datetime"]),
                "end_time": None,
                "duration": None,
                "calculated_auh": 0.0,
            }
            await self.repo.add_job(job_doc)

        elif job["event"] == "completed":

            existing_entry = await self.repo.find_job(job["id"], job["type"])

            end_time = datetime.fromisoformat(job["datetime"])
            duration = end_time - existing_entry["start_time"]
            calculated_auh = AUHCalculator.calculate(
                existing_entry["type"], duration, job["event"]
            )

            duration_hours = duration.total_seconds() / 3600

            updates = {
                "status": "completed",
                "end_time": end_time,
                "duration": duration_hours,
                "calculated_auh": calculated_auh,
            }
            result = await self.repo.update_job(job["id"], job["type"], 
                                                updates)

            if result:
                await self.fia_compliance_repository.increment_total(
                    start_time=existing_entry["start_time"], auh=calculated_auh
                )

        else:
            return None
