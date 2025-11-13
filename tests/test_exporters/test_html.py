"""Unit tests for HTML exporter."""

from pathlib import Path

import pytest

from chatmark.exporters.html import HTMLExporter


class TestHTMLExporter:
    """Tests for HTMLExporter."""

    def test_exporter_instantiation(self):
        """Test that exporter can be instantiated."""
        exporter = HTMLExporter()
        assert exporter is not None

    def test_export_creates_html_file(self, temp_output_dir: Path):
        """Test that export creates an HTML file."""
        exporter = HTMLExporter()
        content = "**User**\n\nTest\n\n**AI**\n\nResponse"
        output_path = str(temp_output_dir / "test.html")
        result = exporter.export(content, output_path)
        assert Path(result).exists()
        assert Path(result).suffix == ".html"

    def test_export_generates_valid_html(self, temp_output_dir: Path):
        """Test that exported HTML is valid."""
        exporter = HTMLExporter()
        content = "**User**\n\nTest\n\n**AI**\n\nResponse"
        output_path = str(temp_output_dir / "test.html")
        exporter.export(content, output_path)
        html_content = Path(output_path).read_text()
        assert "<!DOCTYPE html>" in html_content
        assert "<html" in html_content

    def test_export_preserves_content(self, temp_output_dir: Path):
        """Test that content is preserved in HTML."""
        exporter = HTMLExporter()
        content = "**User**\n\nQuestion\n\n**AI**\n\nAnswer"
        output_path = str(temp_output_dir / "test.html")
        exporter.export(content, output_path)
        html_content = Path(output_path).read_text()
        assert "Question" in html_content
        assert "Answer" in html_content

    def test_export_includes_css(self, temp_output_dir: Path):
        """Test that exported HTML includes CSS styling."""
        exporter = HTMLExporter()
        content = "**User**\n\nTest\n\n**AI**\n\nResponse"
        output_path = str(temp_output_dir / "test.html")
        exporter.export(content, output_path)
        html_content = Path(output_path).read_text()
        assert "<style>" in html_content
        assert ":root" in html_content

