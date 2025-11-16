# api/api.py
from fastapi import FastAPI
from pymongo import MongoClient
from infrastructure.job_repository import JobRepository
from application.job_service import JobService

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
repo = JobRepository(client)
service = JobService(repo)

@app.get("/jobs/summary")
def get_job_summary():
    summary = service.get_summary()
    return summary.to_dict()
