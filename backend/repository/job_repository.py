# repositories/job_repository.py
from ..db.mongo import jobs_collection


class JobRepository:
    def add_job(self, job_doc):
        jobs_collection.insert_one(job_doc)

    def update_job(self, job_id, updates):
        jobs_collection.update_one({"job_id": job_id}, {"$set": updates})

    def find_job(self, job_id):
        return jobs_collection.find_one({"job_id": job_id})
    