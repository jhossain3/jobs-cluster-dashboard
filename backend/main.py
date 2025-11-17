from fastapi import FastAPI
from backend.routers import summary_api
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(summary_api.router, prefix="/summary")
# app.include_router(fia_compliance_api.router, prefix="/compliance")
