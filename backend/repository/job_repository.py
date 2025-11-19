# repositories/job_repository.py
from ..db.mongo import jobs_collection


class JobRepository:
    
    def __init__(self):
        self.jobs_collection = jobs_collection

    #insert entry into jobs collection
    async def add_job(self, job_doc):
        await self.jobs_collection.insert_one(job_doc)

    #update job entry in jobs collection
    async def update_job(self, job_id, job_type, updates):
        result = await self.jobs_collection.update_one(
            {"job_id": job_id, "type": job_type}, {"$set": updates}
        )
        return result.modified_count > 0  # return true if update happened

    #find job by id and type
    async def find_job(self, job_id, job_type):
        if job_type:
            query = {
                "job_id": job_id,
                "type": job_type,
            }
            return await self.jobs_collection.find_one(query)
        return await self.jobs_collection.find_one({"job_id": job_id})
