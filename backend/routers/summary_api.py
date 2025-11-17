from fastapi import APIRouter, Query
from ..repository.summary_repository import SummaryRepository
from datetime import datetime

router = APIRouter()


@router.get("/report")
def summary_report(
    start_date: str = Query(..., description="ISO datetime string"),
    end_date: str = Query(..., description="ISO datetime string"),
):
    repo = SummaryRepository()

    report = repo.get_summary(
        start_date=datetime.fromisoformat(start_date),
        end_date=datetime.fromisoformat(end_date),
    )
    print("summary_report", report)
    return report
