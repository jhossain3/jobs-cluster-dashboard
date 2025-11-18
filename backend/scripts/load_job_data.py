import json
from ..services.event_handler import EventService
import asyncio

# Initialize the service
event_service = EventService()

# Load events from JSON file
with open("backend/data/job_events.json", "r", encoding="utf-8") as f:
    events = json.load(f)


async def main():
    for event in events:
        await event_service.handle_event(event)

asyncio.run(main())

