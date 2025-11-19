import pytest
from unittest.mock import Mock, AsyncMock
from datetime import datetime, timedelta
from backend.repository.summary_repository import SummaryRepository

@pytest.mark.asyncio
async def test_get_summary_with_mesh_solve_postpro():
    # Arrange: fake jobs with calculated_auh values
    fake_jobs = [
        {"id": 1356, "event": "completed", "datetime": "2025-10-01T01:50:37", "type": "mesh", "calculated_auh": 100.0},
        {"id": 2268, "event": "completed", "datetime": "2025-10-01T01:52:44", "type": "mesh", "calculated_auh": 200.0},
        {"id": 2430, "event": "completed", "datetime": "2025-10-01T02:59:35", "type": "solve", "calculated_auh": 5120.0},
        {"id": 5555, "event": "completed", "datetime": "2025-10-01T03:10:00", "type": "postpro", "calculated_auh": 640.0},
    ]

    mesh_total = sum(job["calculated_auh"] for job in fake_jobs if job["type"] == "mesh")
    solve_total = sum(job["calculated_auh"] for job in fake_jobs if job["type"] == "solve")
    postpro_total = sum(job["calculated_auh"] for job in fake_jobs if job["type"] == "postpro")
    grand_total = mesh_total + solve_total + postpro_total

    fake_results = [{
        "auh_by_type": [
            {"_id": "mesh", "total_auh": mesh_total},
            {"_id": "solve", "total_auh": solve_total},
            {"_id": "postpro", "total_auh": postpro_total},
        ],
        "overall": [
            {"_id": None, "grand_total_auh": grand_total}
        ]
    }]
    
    mock_cursor = Mock()
    mock_cursor.to_list = AsyncMock(return_value=fake_results)
    mock_collection = Mock()
    mock_collection.aggregate.return_value = mock_cursor

    repo = SummaryRepository()
    repo.collection = mock_collection

    start_date = datetime(2025, 10, 1, 0, 0, 0)
    end_date = start_date + timedelta(days=1)

    # Act
    summary = await repo.get_summary(start_date, end_date)

    # Assert: check each type and the grand total
    by_type = {item["_id"]: item["total_auh"] for item in summary["auh_by_type"]}
    assert by_type["mesh"] == mesh_total
    assert by_type["solve"] == solve_total
    assert by_type["postpro"] == postpro_total
    assert summary["overall"][0]["grand_total_auh"] == grand_total

