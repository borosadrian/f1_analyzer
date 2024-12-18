from typing import Optional, Any, TypedDict
from abc import abstractmethod
import pandas as pd
import numpy as np
import logging
import matplotlib.pyplot as plt

from .base_analyzer import BaseAnalyzer

logger = logging.getLogger(__name__)


class AnalyzeResult(TypedDict):
    identifier: str
    year: int
    round: int
    average_lap_time: float
    fastest_lap: float
    lap_time_variance: float


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

    def get_lap_times_dropna(self) -> pd.Series:
        """

        :return: Clean lap times (without any nan values
        """
        return self.laps['LapTime'].dropna().dt.total_seconds()

    @abstractmethod
    def compare_lap_times(self, other: str, stint: int = None):
        """
        Abstract method, compares stint lap times to another driver/team stint lap times depending on where it is implemented
        :param other: The driver/team whose lap times we want to compare with the current driver
        :param stint: The specific stint number to filter lap times (default is None to include all laps)
        :return: DataFrame containing lap number, first (driver/team) lap time, second (driver/team) lap time
        """
        pass

    def calculate_lap_time_variance(self) -> float:
        """
        Calculates variance of lap time, lower variance means more consistent laps
        :return: Varience of lap times
        """
        lap_times = self.get_lap_times_dropna()
        filtered_lap_times = self.filter_lap_outliers(lap_times)
        filtered_lap_times = pd.Series(filtered_lap_times)
        return filtered_lap_times.var()

    def calculate_lap_times_percentile(self, percentile: list = [25, 50, 75]) -> dict:
        """
        Calculates percentiles of lap times
        :param percentile: list of percentiles to calculate, default is 25, 50, 75
        :return: Dictionary of selected percentile and its value
        """
        lap_times = self.get_lap_times_dropna()
        filtered_lap_times = self.filter_lap_outliers(lap_times)
        filtered_lap_times = pd.Series(filtered_lap_times)
        percentile_values = {p: np.percentile(filtered_lap_times, p) for p in percentile}
        return percentile_values

    def lap_time_progression(self) -> pd.DataFrame:
        """
        Calculates time differences between laps
        :return: DataFrame with lap number, lap times, time change by lap
        """
        progression = self.laps[['LapNumber', 'LapTimes']].dropna()
        progression['LapTimeSeconds'] = progression['LapTimes'].dt.total_seconds()
        progression = progression.sort_values(by='LapNumber')
        progression['TimeChange'] = progression['LapTimeSeconds'].diff()
        return progression

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
        lap_times = self.get_lap_times_dropna()
        clean_lap_times = self.filter_lap_outliers(lap_times)

        if len(clean_lap_times) == 0:
            logger.info(f"No valid lap times after filtering for {self.identifier} in {self.session.event['EventName']}")
        else:
            logger.info(f"Valid lap times for {self.identifier} in {self.session.event['EventName']}: {clean_lap_times}")

        if clean_lap_times:
            return np.median(clean_lap_times)
        return np.nan

    def plot_lap_time_progression(self):
        progression = self.lap_time_progression()
        plt.figure(figsize=(10, 6))
        plt.plot(progression['LapNumber'], progression['LapTimeSeconds'], label='Lap Time (s)')
        plt.xlabel('Lap Number')
        plt.ylabel('Lap Time (Sec)')
        plt.title(f'Lap Time Progression for {self.identifier} - {self.year} Round {self.round_number}')
        plt.grid(True)
        plt.legend()
        plt.show()

    def analyze(self) -> AnalyzeResult:
        """
        Analyzes lap times and returns average lap time, fastest lap, lap time variance.
        :return: Dictionary with identifier, session info, average and fastest lap and lap time variance
        """
        if self.laps is None:
            self.load_data()

        assert isinstance(self.laps, pd.DataFrame)
        # Don't know how to tell mypy that self.laps is not "DataFrame | None", but it is actually "DataFrame"
        avg_lap_time = self.get_average_lap_time()
        lap_time_variance = self.calculate_lap_time_variance()
        fastest_lap = self.laps['LapTime'].min().total_seconds()

        return {
            "identifier": self.identifier,
            "year": self.year,
            "round": self.round_number,
            "average_lap_time": avg_lap_time,
            "fastest_lap": fastest_lap,
            "lap_time_variance": lap_time_variance
        }
