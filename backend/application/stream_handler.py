# application/stream_handler.py
from application.event_processor_factory import EventProcessorFactory
from repository.job_repository import JobRepository


def handle_stream(events):
    repo = JobRepository()
    factory = EventProcessorFactory(repo)

    for event in events:
        processor = factory.get_processor(event)
        processor.process(event)
