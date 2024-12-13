import logging
from .base_analyzer import BaseAnalyzer
import fastf1

logger = logging.getLogger(__name__)


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
        self.session = None # For session data
        self.laps = None  # For loaded lap data

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
        self.session.load()
        logger.info(f"Data loaded for session year {self.year} round {self.round_number}")

    def load_data(self) -> None:
        """
        Calls load_session() and assigns driver laps data to self.laps
        """
        self.load_session()
        logger.info(f"Loading data for {self.driver_code}, {self.year} round {self.round_number}")
        self.laps = self.session.laps.pick_drivers(self.driver_code)
        logger.info(f"Data loaded for {self.driver_code}. Found {len(self.laps)} laps.")

    def analyze(self) -> dict[str, str | int]:
        """
        Performs simple analyse on specified driver. Will be extended later.
        :return: For now returns dict with driver and session info, number of laps of specified driver.
        """

        if self.laps is None:
            logger.warning(f"No laps loaded. Calling load_data()")
            self.load_data()

        return {
            "driver": self.driver_code,
            "year": self.year,
            "round": self.round_number,
            "laps_count": len(self.laps) if self.laps is not None else 0
        }