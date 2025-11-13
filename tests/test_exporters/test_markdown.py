"""Unit tests for markdown exporter."""

from pathlib import Path

from chatmark.exporters.markdown import MarkdownExporter


class TestMarkdownExporter:
    """Tests for MarkdownExporter."""

    def test_exporter_instantiation(self):
        """Test that exporter can be instantiated."""
        exporter = MarkdownExporter()
        assert exporter is not None

    def test_export_creates_markdown_file(self, temp_output_dir: Path):
        """Test that export creates a markdown file."""
        exporter = MarkdownExporter()
        content = "**User**\n\nTest\n\n**AI**\n\nResponse"
        output_path = str(temp_output_dir / "test.md")
        result = exporter.export(content, output_path)
        assert Path(result).exists()
        assert Path(result).suffix == ".md"

    def test_export_passes_through_internal_format_exactly(self, temp_output_dir: Path):
        """Test that exporter passes through internal format without transformation."""
        exporter = MarkdownExporter()
        content = "**User**\n\nQuestion\n\n**AI**\n\nAnswer"
        output_path = str(temp_output_dir / "test.md")
        exporter.export(content, output_path)
        exported_content = Path(output_path).read_text()
        assert exported_content == content

    def test_export_preserves_markers(self, temp_output_dir: Path):
        """Test that User/AI markers are preserved exactly."""
        exporter = MarkdownExporter()
        content = "**User**\n\nTest\n\n**AI**\n\nResponse"
        output_path = str(temp_output_dir / "test.md")
        exporter.export(content, output_path)
        exported_content = Path(output_path).read_text()
        assert "**User**" in exported_content
        assert "**AI**" in exported_content

    def test_export_preserves_formatting(self, temp_output_dir: Path):
        """Test that markdown formatting is preserved."""
        exporter = MarkdownExporter()
        content = "**User**\n\nQuestion with **bold** text\n\n**AI**\n\n```python\ncode\n```"
        output_path = str(temp_output_dir / "test.md")
        exporter.export(content, output_path)
        exported_content = Path(output_path).read_text()
        assert "**bold**" in exported_content
        assert "```python" in exported_content
        assert "code" in exported_content
        assert "```" in exported_content

    def test_export_preserves_multiple_exchanges(self, temp_output_dir: Path):
        """Test that multiple User/AI exchanges are preserved."""
        exporter = MarkdownExporter()
        content = (
            "**User**\n\nFirst question\n\n**AI**\n\nFirst answer\n\n"
            "**User**\n\nSecond question\n\n**AI**\n\nSecond answer"
        )
        output_path = str(temp_output_dir / "test.md")
        exporter.export(content, output_path)
        exported_content = Path(output_path).read_text()
        assert exported_content == content
        assert exported_content.count("**User**") == 2
        assert exported_content.count("**AI**") == 2

    def test_export_handles_empty_content(self, temp_output_dir: Path):
        """Test that empty content is handled."""
        exporter = MarkdownExporter()
        content = ""
        output_path = str(temp_output_dir / "test.md")
        exporter.export(content, output_path)
        exported_content = Path(output_path).read_text()
        assert exported_content == ""

    def test_export_round_trip_compatibility(self, temp_output_dir: Path):
        """Test round-trip compatibility: parse → internal format → markdown export."""
        from chatmark.parsers.cursor_md import CursorMarkdownParser

        exporter = MarkdownExporter()
        parser = CursorMarkdownParser()

        # Original Cursor markdown
        original = "**User**\n\nQuestion\n\n**Cursor**\n\nAnswer"
        # Parse to internal format
        internal_format = parser.parse(original)
        # Export to markdown
        output_path = str(temp_output_dir / "test.md")
        exporter.export(internal_format, output_path)
        exported_content = Path(output_path).read_text()

        # Exported markdown should match internal format exactly
        assert exported_content == internal_format
        # Internal format should have **AI** (normalized from **Cursor**)
        assert "**AI**" in exported_content
        assert "**Cursor**" not in exported_content

    def test_export_preserves_whitespace(self, temp_output_dir: Path):
        """Test that whitespace is preserved exactly."""
        exporter = MarkdownExporter()
        content = "**User**\n\n  Indented text\n\n**AI**\n\nResponse with\nmultiple\nlines"
        output_path = str(temp_output_dir / "test.md")
        exporter.export(content, output_path)
        exported_content = Path(output_path).read_text()
        assert exported_content == content
        assert "  Indented text" in exported_content
        assert "multiple\nlines" in exported_content

    def test_export_preserves_code_blocks(self, temp_output_dir: Path):
        """Test that code blocks are preserved exactly."""
        exporter = MarkdownExporter()
        content = "**User**\n\nShow code\n\n**AI**\n\n```python\ndef hello():\n    print('hi')\n```"
        output_path = str(temp_output_dir / "test.md")
        exporter.export(content, output_path)
        exported_content = Path(output_path).read_text()
        assert exported_content == content
        assert "```python" in exported_content
        assert "def hello():" in exported_content
        assert "    print('hi')" in exported_content
        assert "```" in exported_content
