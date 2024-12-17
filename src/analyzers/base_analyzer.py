from abc import ABC, abstractmethod
import logging
from typing import Any, Optional
import fastf1  # type: ignore
import pandas as pd

logger = logging.getLogger(__name__)


class BaseAnalyzer(ABC):
    """BaseAnalyzer is an abstract class defining interface for all performance analyzers"""
    def __init__(self, identifier: str, year: int, round_number: int, session_identifier: str) -> None:
        """
        Initialize general analyzer for selected year and round number
        :param identifier: Three letter identifier of team or driver, depending on the analysis type
        :param year: Year of the season, e.g. 2024
        :param round_number: Ordinal number of the race (1 = first race of the season)
        """
        self.identifier = identifier
        self.year = year
        self.round_number = round_number
        self.session_identifier = session_identifier
        self.session: Optional[pd.DataFrame] = None

    def load_session(self) -> None:
        """
        Loads the session data using FastF1 for the specified session.
        """
        logger.info(f"Loading session data for year {self.year}, round {self.round_number}")
        self.session = fastf1.get_session(self.year, self.round_number, self.session_identifier)
        assert self.session is not None
        self.session.load()
        logger.info(f"Data loaded for session year {self.year}, round {self.round_number}")

    @staticmethod
    def validate_driver_code(code: str) -> bool:
        return len(code) == 3 and code.isalpha()

    @abstractmethod
    def load_data(self) -> None:
        """
        Loads data for a specified driver or a team
        """
        pass

    @abstractmethod
    def analyze(self) -> Any:
        """
        Performs an analysis and returns the result
        Result might be DataFrame, dict, or any other data type - will be specified
        :return: Any type
        """
        pass

