"""Abstract base class for parsers."""

from abc import ABC, abstractmethod


class BaseParser(ABC):
    """Abstract base class for parsers that convert input formats to internal markdown format.

    All parsers must implement the parse() method which converts their specific input format
    to the tool's internal markdown format standard (using **User** and **AI** markers).
    """

    @abstractmethod
    def parse(self, content: str) -> str:
        """Parse input content and convert to internal markdown format standard.

        Args:
            content: Input content in the parser's specific format.

        Returns:
            String in internal markdown format standard with **User** and **AI** markers.
        """
        pass
