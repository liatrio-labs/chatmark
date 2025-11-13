"""Cursor markdown parser that normalizes Cursor exports to internal markdown format."""

import re

from chatmark.parsers.base import BaseParser


class CursorMarkdownParser(BaseParser):
    """Parser for Cursor markdown format that normalizes to internal markdown format standard.

    This parser converts Cursor markdown exports (which use **Cursor** markers) to the
    tool's internal markdown format standard (which uses **AI** markers for all AI responses).
    """

    def parse(self, content: str) -> str:
        """Parse Cursor markdown and normalize **Cursor** markers to **AI**.

        Args:
            content: Cursor markdown content with **User** and **Cursor** markers.

        Returns:
            Markdown string in internal format standard with **User** and **AI** markers.
        """
        if not content:
            return ""

        # Normalize **Cursor** to **AI** (case-insensitive)
        # Pattern matches **Cursor** or **CURSOR** etc.
        normalized = re.sub(
            r"\*\*Cursor\*\*",
            "**AI**",
            content,
            flags=re.IGNORECASE,
        )

        return normalized

