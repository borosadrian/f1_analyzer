from typing import Any, TypedDict

from time_based_analyzer import TimeBasedAnalyzer, AnalyzeResult
import logging

logger = logging.getLogger(__name__)


class TeamAnalyzer(TimeBasedAnalyzer):
    """
    Class for analyzing data for an entire team.
    """

    def __init__(self, team_code: str, year: int, round_number: int, session_identifier: str):
        super().__init__(team_code, year, round_number, session_identifier)

    def load_data(self) -> None:
        super().load_data()
        logger.info(f"Loading data for team {self.identifier}, {self.year} round {self.round_number}")
        assert self.session is not None
        self.laps = self.session.laps.pick_teams(self.identifier)
        logger.info(f"Data loaded for {self.identifier}. Found {len(self.laps)} laps.")

    def analyze(self) -> AnalyzeResult:
        """
        Performs simple analyse on specified team. Will be extended later.
        :return: Returns dict with team code, year, round number, average lap time, fastest lap time of specified team.
        """
        return super().analyze()

