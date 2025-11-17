# repositories/job_repository.py
from ..db.mongo import jobs_collection


class JobRepository:
    
    def add_job(self, job_doc):
        jobs_collection.insert_one(job_doc)

    def update_job(self, job_id, job_type, updates):
        result = jobs_collection.update_one(
            {"job_id": job_id, "type": job_type},
            {"$set": updates}
        )
        return result.modified_count > 0  #return true if update happened

    def find_job(self, job_id, job_type):
        if job_type:
            query = {
                "job_id": job_id,
                "type": job_type,
            }
            return jobs_collection.find_one(query)
        return jobs_collection.find_one({"job_id": job_id}) 