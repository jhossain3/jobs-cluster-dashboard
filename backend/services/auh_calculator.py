from datetime import timedelta


class AUHCalculator:
    RESOURCES = {
        "mesh": (64, 7.5),
        "solve": (256, 10.0),
        "postpro": (32, 5.0),
    }
    
    ALLOWED_TYPES = {"solve"}

    @classmethod
    def calculate(
        cls, job_type: str, duration: timedelta, event: str
    ) -> float:
        if event != "completed":
            return 0.0
        if job_type not in cls.ALLOWED_TYPES or not duration:
            return 0.0
        if job_type == "solve" and duration:
            cores, clock_speed = cls.RESOURCES[job_type]
            hours = duration.total_seconds() / 3600
            return hours * cores * clock_speed
        return 0.0
