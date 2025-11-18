from motor.motor_asyncio import AsyncIOMotorClient

client: AsyncIOMotorClient = AsyncIOMotorClient("mongodb://localhost:27017/?replicaSet=rs0")

# Choose the database
db = client["jobEventSystem"]

# Choose the collection
jobs_collection = db["jobs"]
fia_compliance_collection = db["eight_week_limit"]
