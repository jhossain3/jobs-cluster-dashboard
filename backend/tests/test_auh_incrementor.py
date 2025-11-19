import pytest
from unittest.mock import AsyncMock
from backend.repository.fia_compliance_repository import FiaComplianceRepository

@pytest.mark.asyncio
async def test_increment_total_updates_collection():
    mock_collection = AsyncMock()
    repo = FiaComplianceRepository()
    repo.fia_compliance_collection = mock_collection
    repo.get_fia_window = AsyncMock(return_value={
        "_id": "abc123",
        "current_auh_count": 10,
        "limit": 100
    })

    await repo.increment_total("2025-10-01T00:00:00", 20)

    mock_collection.update_one.assert_awaited_once_with(
        {"_id": "abc123"},
        {
            "$inc": {"current_auh_count": 20},
            "$set": {"limit_exceeded": False},
        },
    )

@pytest.mark.asyncio
async def test_increment_total_exceeds_limit():
    mock_collection = AsyncMock()
    repo = FiaComplianceRepository()
    repo.fia_compliance_collection = mock_collection
    # Start close to the limit so increment pushes it over
    repo.get_fia_window = AsyncMock(return_value={
        "_id": "xyz789",
        "current_auh_count": 95,
        "limit": 100
    })

    await repo.increment_total("2025-10-01T00:00:00", 10)

    mock_collection.update_one.assert_awaited_once_with(
        {"_id": "xyz789"},
        {
            "$inc": {"current_auh_count": 10},
            "$set": {"limit_exceeded": True},  # 95+10=105 > 100
        },
    )