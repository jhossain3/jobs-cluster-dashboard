import pytest
from datetime import timedelta
from backend.services.auh_calculator import AUHCalculator  # adjust import path

def test_calculate_valid_solve_completed():
    duration = timedelta(hours=2)
    result = AUHCalculator.calculate("solve", duration, "completed")
    # 2 hours * 256 cores * 10.0 clock speed = 5120.0
    assert result == pytest.approx(5120.0)

def test_calculate_non_completed_event():
    duration = timedelta(hours=1)
    result = AUHCalculator.calculate("solve", duration, "running")
    assert result == 0.0

def test_calculate_disallowed_job_type():
    duration = timedelta(hours=1)
    result = AUHCalculator.calculate("mesh", duration, "completed")
    assert result == 0.0

def test_calculate_no_duration():
    result = AUHCalculator.calculate("solve", None, "completed")
    assert result == 0.0

def test_calculate_boundary_one_hour():
    duration = timedelta(hours=1)
    result = AUHCalculator.calculate("solve", duration, "completed")
    # 1 hour * 256 cores * 10.0 clock speed = 2560.0
    assert result == pytest.approx(2560.0)
