from typing import Optional, Any, TypedDict
import pandas as pd
import numpy as np
import logging

from base_analyzer import BaseAnalyzer

logger = logging.getLogger(__name__)


class AnalyzeResult(TypedDict):
    identifier: str
    year: int
    round: int
    average_lap_time: float
    fastest_lap: float


class TimeBasedAnalyzer(BaseAnalyzer):
    """
    Class for analyzing lap times of a specific driver or a team
    """
    def __init__(self, identifier: str, year: int, round_number: int, session_identifier: str) -> None:
        super().__init__(identifier, year, round_number, session_identifier)
        self.laps: Optional[pd.DataFrame] = None


    def load_data(self) -> None:
        """
        Loads lap time data for the driver or team.
        """
        super().load_session()
        logger.info(f"Loading lap times for {self.identifier}")

    @staticmethod
    def filter_lap_outliers(lap_times: pd.Series) -> list:
        """
        Filters out outlier lap times based on a threshold multiplier of standard deviation.
        :param lap_times: Series of lap times in seconds
        :return: List of lap times after filtering out outliers
        """
        median_lap_time = np.median(lap_times)
        threshold = 1.5  # Adjust this multiplier for sensitivity
        return [time for time in lap_times if abs(time - median_lap_time) <= threshold * np.std(lap_times)]

    def get_average_lap_time(self) -> float:
        """
        Calculates average lap time for team or driver, self.laps must be loaded first in child class
        :return: average lap time for team or driver
        """
        lap_times = self.laps['LapTime'].dropna().dt.total_seconds()  # Exclude NaT values
        clean_lap_times = self.filter_lap_outliers(lap_times)

        if len(clean_lap_times) == 0:
            logger.info(f"No valid lap times after filtering for {self.identifier} in {self.session.event['EventName']}")
        else:
            logger.info(f"Valid lap times for {self.identifier} in {self.session.event['EventName']}: {clean_lap_times}")

        if clean_lap_times:
            return np.median(clean_lap_times)
        return np.nan

    def analyze(self) -> AnalyzeResult:
        """
        Analyzes lap times and returns average lap time and fastest lap.
        """
        if self.laps is None:
            self.load_data()

        assert isinstance(self.laps, pd.DataFrame)
        # Don't know how to tell mypy that self.laps is not "DataFrame | None", but it is actually "DataFrame"
        avg_lap_time = self.get_average_lap_time()
        fastest_lap = self.laps['LapTime'].min().total_seconds()

        return {
            "identifier": self.identifier,
            "year": self.year,
            "round": self.round_number,
            "average_lap_time": avg_lap_time,
            "fastest_lap": fastest_lap
        }

    def analyze_lap_differences(self) -> pd.DataFrame:
        """
        Analyzes the lap time differences between the laps.
        """
        if self.laps is None:
            self.load_data()

        # Calculate the differences between consecutive laps
        self.laps['lap_diff'] = self.laps['LapTime'].diff().dt.total_seconds()
        return self.laps[['LapNumber', 'lap_diff']]
