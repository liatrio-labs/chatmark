"""Abstract base class for exporters."""

from abc import ABC, abstractmethod


class BaseExporter(ABC):
    """Abstract base class for exporters that convert internal markdown format to output formats.

    All exporters must implement the export() method which converts the internal markdown
    format standard (using **User** and **AI** markers) to their specific output format.
    """

    @abstractmethod
    def export(self, content: str, output_path: str) -> str:
        """Export internal markdown format to output format.

        Args:
            content: Content in internal markdown format standard with **User** and **AI** markers.
            output_path: Path where the exported file should be written.

        Returns:
            Path to the created output file.
        """
        pass

