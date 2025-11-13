"""HTML exporter that converts internal markdown format to HTML."""

from pathlib import Path

from chatmark.core.converter import convert_markdown_to_html
from chatmark.exporters.base import BaseExporter


class HTMLExporter(BaseExporter):
    """Exporter that converts internal markdown format to HTML output.

    This exporter uses the core converter to generate HTML files with Liatrio styling.
    """

    def export(self, content: str, output_path: str) -> str:
        """Export internal markdown format to HTML file.

        Args:
            content: Content in internal markdown format standard with **User** and **AI** markers.
            output_path: Path where the HTML file should be written.

        Returns:
            Path to the created HTML file.
        """
        # Write content to temporary markdown file
        temp_md = Path(output_path).with_suffix(".tmp.md")
        temp_md.parent.mkdir(parents=True, exist_ok=True)
        temp_md.write_text(content, encoding="utf-8")

        # Convert markdown to HTML using core converter
        output_file = Path(output_path)
        try:
            result = convert_markdown_to_html(temp_md, output_file)
        finally:
            # Clean up temporary file even if conversion fails
            if temp_md.exists():
                temp_md.unlink()

        return str(result)
