from fastapi import APIRouter, Query
from ..repository.summary_repository import SummaryRepository
from datetime import datetime

router = APIRouter()

#route to generate summary report on auh totals per type and overall total
@router.get("/report")
async def summary_report(
    start_date: str = Query(..., description="ISO datetime string"),
    end_date: str = Query(..., description="ISO datetime string"),
):
    repo = SummaryRepository()

    report = await repo.get_summary(
        start_date=datetime.fromisoformat(start_date),
        end_date=datetime.fromisoformat(end_date),
    )
    print("summary_report", report)
    return report
