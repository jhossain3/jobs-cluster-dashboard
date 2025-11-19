# jobs-cluster-dashboard

--- 
## Welcome welcome

Hi Mercedes-AMG Petronas team,

Welcome to my repo! It's been an immense privilege to reach this stage of the interview — thank you for the opportunity. I had a lot of fun working through this assignment. Yes, it kept me up at night … but honestly, what good coding problem doesn’t?

Designing something from the ground up, breaking things, fixing them, and iterating over the span of a week was incredibly exciting — and gave me a tiny taste of what it must feel like to build cool things with your team.

Below you’ll find instructions for running the codebase, plus some notes on limitations I ran into with time and resources.

Looking forward to hearing from you — ciao!

## instructions to run 

### 1. Setup Virtual Environment (root directory)


python3 -m venv venv
source venv/bin/activate

### 2. Mongo DB setup (run in terminal open)

docker-compose up -d
docker exec -it mongodb mongosh

rs.initiate()
rs.status()
cfg = rs.conf()
cfg.members[0].host = "mongo:27017"
rs.reconfig(cfg, {force: true})



use jobEventSystem
db.createCollection("eight_week_limit")
db.createCollection("jobs")

db.eight_week_limit.insertOne({
  start_date: new Date("2025-10-01T00:00:00Z"),
  end_date: new Date("2025-11-26T00:00:00Z"),
  current_auh_count: 0,
  limit: 10000000,
  limit_exceeded: false
})


### 3. Frontend setup

cd frontend
npm install
npm run start

### 4. Backend setup

(with source venv/bin/activate in root)
cd backend
pip install -r requirements.txt
pip install 'uvicorn[standard]'

cd root
uvicorn backend.main:app --reload

### 6. Load Job Data

when you run this 
python3 -m backend.scripts.load_job_data    

you can see the db update in real time at:

http://localhost:8000/compliance/currentstatus

The data streams in live which can be seen by refreshing the endpoint

once you see the limit_exceeded field switch to true, this will automatically
trigger a pop up in the frontend to alert the user the auh limit is exceeded which is
replaced by a persistent banner onclose


## Limitations

due to time/resource constraints I was unable to implement the following:

- implementing a Kafka consumer instead of listener script to handle detection of limit exceeded
- component to show AUH remaining in time window
- instead of hardcoding the time window limit this should talk to an api to pull the constraints from the fia to reduce human error 
- global styling
- further component modularisation such as DatePicker modal
- security testing and safeguarding

