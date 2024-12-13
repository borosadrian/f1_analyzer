from abc import ABC, abstractmethod
import logging
from typing import Any

class BaseAnalyzer(ABC):
    """BaseAnalyzer is an abstract class defining interface for all performance analyzers"""

    @abstractmethod
    def analyze(self) -> Any:
        """
        Performs an analysis and returns the result
        Result might be DataFrame, dict, or any other data type - will be specified
        :return: Any type
        """
        pass
