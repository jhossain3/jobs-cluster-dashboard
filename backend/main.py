from fastapi import FastAPI
from backend.routers import summary_api, fia_compliance_api
from backend.services.compliance_listener import watch_limit_exceeded

from fastapi.middleware.cors import CORSMiddleware
import asyncio

# Define lifespan event to start and stop the MongoDB change stream listener
async def lifespan(app: FastAPI):
    # Startup
    task = asyncio.create_task(watch_limit_exceeded())
    print("Started MongoDB change stream listener")

    yield  

    # Shutdown
    task.cancel()
    print("Stopped MongoDB change stream listener")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers calling api endpoints

app.include_router(summary_api.router, prefix="/summary")
app.include_router(fia_compliance_api.router, prefix="/compliance")
