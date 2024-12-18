import pytest
import pandas as pd
from unittest.mock import MagicMock
from src.analyzers.time_based_analyzer import TimeBasedAnalyzer


@pytest.fixture
def time_based_analyzer():
    analyzer = TimeBasedAnalyzer('VER', 2024, 1, 'R')
    analyzer.session = MagicMock()
    analyzer.laps = pd.DataFrame({
        'LapTime': pd.to_timedelta([90, 85, 88, 95, 120, 87])
    })
    return analyzer


def test_get_average_lap_time(time_based_analyzer: TimeBasedAnalyzer):

    avg_lap_time = time_based_analyzer.get_average_lap_time()
    assert isinstance(avg_lap_time, float), f"Expected float, got {type(avg_lap_time)}"
    assert avg_lap_time > 0, f"Expected positive value, got {avg_lap_time}"


def test_filter_lap_outliers(time_based_analyzer):
    lap_times = time_based_analyzer.laps['LapTime'].dt.total_seconds()
    filtered_times = time_based_analyzer.filter_lap_outliers(lap_times)
    assert len(filtered_times) == 5, f"Expected 5 laps after filtering, got {len(filtered_times)}"
