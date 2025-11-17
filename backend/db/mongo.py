from pymongo import MongoClient

# Create a client connection to MongoDB
client: MongoClient = MongoClient("mongodb://localhost:27017")

# Choose the database
db = client["jobEventSystem"]

# Choose the collection
jobs_collection = db["jobs"]
fia_compliance_collection = db["eight_week_limit"]
