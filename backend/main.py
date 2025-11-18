from fastapi import FastAPI, WebSocket
from backend.routers import summary_api, fia_compliance_api
from backend.db.mongo import fia_compliance_collection
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(summary_api.router, prefix="/summary")
app.include_router(fia_compliance_api.router, prefix="/compliance")
