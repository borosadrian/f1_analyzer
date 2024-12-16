import pytest
from analyzers.driver_analyzer import DriverAnalyzer

def test_driver_analyzer_basic():
    analyzer = DriverAnalyzer(driver_code="VER", year=2024, round_number=1)
    result = analyzer.analyze()

    assert "driver" in result
    assert "year" in result
    assert "round" in result
    assert "laps_count" in result

    assert result["driver"] == "VER"
    assert result["year"] == 2024
    assert result["round"] == 1
    assert isinstance(result["laps_count"], int)

@pytest.mark.parametrize("driver_code,year,round_number,expected_laps_count", [
    ("VER", 2024, 1, 57),
    ("NOR", 2024, 1, 57),
    ("HAM", 2024, 2, 50)
])

def test_mulptiple_drivers(driver_code, year, round_number, expected_laps_count):
    analyzer = DriverAnalyzer(driver_code=driver_code, year=year, round_number=round_number)
    result = analyzer.analyze()
    assert result["driver"] == driver_code
    assert result["year"] == year
    assert result["round"] == round_number
    assert result["laps_count"] == expected_laps_count