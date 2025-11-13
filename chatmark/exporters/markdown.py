"""Markdown exporter that outputs the exact internal markdown format standard.

This exporter provides round-trip compatibility by outputting the exact internal
markdown format standard without modification. This ensures that exported markdown
can be re-imported with `--format cursor-md` and converted to HTML/PDF later.
"""

from pathlib import Path

from chatmark.exporters.base import BaseExporter


class MarkdownExporter(BaseExporter):
    """Exporter that outputs internal markdown format standard without transformation.

    This exporter passes through the internal markdown format exactly as-is,
    ensuring round-trip compatibility for markdown exports.
    """

    def export(self, content: str, output_path: str) -> str:
        """Export internal markdown format to markdown file.

        Args:
            content: Content in internal markdown format standard with **User** and **AI** markers.
            output_path: Path where the markdown file should be written.

        Returns:
            Path to the created markdown file.
        """
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return str(path)

