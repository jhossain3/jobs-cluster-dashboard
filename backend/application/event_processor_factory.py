# application/event_processor_factory.py
from repository.start_event_processor import StartEventProcessor
from repository.completed_event_processor import CompletedEventProcessor


class EventProcessorFactory:
    def __init__(self, repository):
        self.repository = repository

    def get_processor(self, event):
        if event["event"] == "start":
            return StartEventProcessor(self.repository)
        elif event["event"] == "completed":
            return CompletedEventProcessor(self.repository)
        else:
            raise ValueError(f"Unknown event type: {event['event']}")
