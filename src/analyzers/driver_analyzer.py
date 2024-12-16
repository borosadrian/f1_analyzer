from typing import Optional, TypedDict, cast
import logging

import pandas as pd

from base_analyzer import BaseAnalyzer
import fastf1  # type: ignore

logger = logging.getLogger(__name__)


class AnalyzeResult(TypedDict):
    driver: str
    year: int
    round: int
    laps_count: int


class DriverAnalyzer(BaseAnalyzer):
    """
    Analyzer for specific driver. Allows to read data from FastF1 for selected season and race
    and perform analysis
    """

    def __init__(self, driver_code: str, year: int, round_number: int) -> None:
        """
        Initialize analyzer for specific driver
        :param driver_code: Three letter code of a driver, e.g. "VER" or "HAM"
        :param year: Year of the season, e.g. 2024
        :param round_number: Ordinal number of the race (1 = first race of the season)
        """
        if not self.validate_driver_code(driver_code):
            raise ValueError(f"Invalid driver code: {driver_code}")
        self.driver_code = driver_code
        self.year = year
        self.round_number = round_number

        self.session: Optional[fastf1.core.Session] = None # For session data
        self.laps: Optional[pd.DataFrame] = None  # For loaded lap data

    @staticmethod
    def validate_driver_code(code: str) -> bool:
        return len(code) == 3 and code.isalpha()

    def load_session(self) -> None:
        """
        Loads race session data for a specified year and round number
        """
        logger.info(f"Loading session data for year {self.year} round {self.round_number}")
        fastf1.Cache.enable_cache('cache')
        self.session = fastf1.get_session(self.year, self.round_number, 'R')  # identifier R = Race data
        assert self.session is not None
        self.session.load()
        logger.info(f"Data loaded for session year {self.year} round {self.round_number}")

    def load_data(self) -> None:
        """
        Calls load_session() and assigns driver laps data to self.laps
        """
        self.load_session()
        logger.info(f"Loading data for {self.driver_code}, {self.year} round {self.round_number}")
        assert self.session is not None
        self.laps = self.session.laps.pick_drivers(self.driver_code)
        logger.info(f"Data loaded for {self.driver_code}. Found {len(self.laps)} laps.")

    def analyze(self) -> AnalyzeResult:
        """
        Performs simple analyse on specified driver. Will be extended later.
        :return: For now returns dict with driver and session info, number of laps of specified driver.
        """

        if self.laps is None:
            logger.warning(f"No laps loaded. Calling load_data()")
            self.load_data()

        if isinstance(self.laps, pd.DataFrame):
            return {
                "driver": self.driver_code,
                "year": self.year,
                "round": self.round_number,
                "laps_count": len(self.laps)
            }

        return {
            "driver": self.driver_code,
            "year": self.year,
            "round": self.round_number,
            "laps_count": 0
        }

