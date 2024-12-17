from typing import Optional, TypedDict
import logging

import pandas as pd

from time_based_analyzer import TimeBasedAnalyzer, AnalyzeResult
import fastf1  # type: ignore

logger = logging.getLogger(__name__)


class DriverTimeBasedAnalyzer(TimeBasedAnalyzer):
    """
    Analyzer for specific driver. Allows to read data from FastF1 for selected season and race
    and perform time analysis
    """

    def __init__(self, driver_code: str, year: int, round_number: int, session_identifier: str) -> None:
        """
        Initialize analyzer for specific driver
        :param driver_code: Three letter code of a driver, e.g. "VER" or "HAM"
        :param year: Year of the season, e.g. 2024
        :param round_number: Ordinal number of the race (1 = first race of the season)
        """
        super().__init__(driver_code, year, round_number, session_identifier)

    def load_data(self) -> None:
        """
        Calls load_session() and assigns driver laps data to self.laps
        """
        self.load_session()
        logger.info(f"Loading data for {self.identifier}, {self.year} round {self.round_number}")
        assert self.session is not None
        self.laps = self.session.laps.pick_drivers(self.identifier)
        logger.info(f"Data loaded for {self.identifier}. Found {len(self.laps)} laps.")

    def analyze(self) -> AnalyzeResult:
        """
        Performs simple analyse on specified driver. Will be extended later.
        :return: Returns dict with team code, year, round number, average lap time, fastest lap time of specified driver.
        """
        return super().analyze()

