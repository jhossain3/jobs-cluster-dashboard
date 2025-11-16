import json
from ..services.event_handler import EventService

# Initialize the service
event_service = EventService()

# Load events from JSON file
with open("backend/data/job_events.json", "r", encoding="utf-8") as f:
    events = json.load(f)

for event in events:
    job = event_service.handle_event(event)
    print(job)
