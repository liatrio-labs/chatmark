"""Unit tests for converter orchestration."""

from pathlib import Path

import pytest

from chatmark.core.converter import convert_markdown_to_html


class TestConvertMarkdownToHtml:
    """Tests for convert_markdown_to_html function."""

    def test_converts_markdown_to_html(self, cursor_sample_md: Path, temp_output_dir: Path):
        """Test that markdown file is converted to HTML."""
        output_file = temp_output_dir / "test.html"
        result = convert_markdown_to_html(cursor_sample_md, output_file)
        assert result == output_file
        assert output_file.exists()
        assert output_file.read_text().startswith("<!DOCTYPE html>")

    def test_raises_error_for_nonexistent_file(self, temp_output_dir: Path):
        """Test that FileNotFoundError is raised for nonexistent file."""
        nonexistent = temp_output_dir / "nonexistent.md"
        with pytest.raises(FileNotFoundError):
            convert_markdown_to_html(nonexistent)

    def test_generates_timestamped_filename_when_no_output_specified(
        self, cursor_sample_md: Path, temp_output_dir: Path
    ):
        """Test that timestamped filename is generated when output not specified."""
        result = convert_markdown_to_html(cursor_sample_md)
        assert result.exists()
        assert result.suffix == ".html"
        assert cursor_sample_md.stem in result.stem

    def test_html_contains_processed_content(self, cursor_sample_md: Path, temp_output_dir: Path):
        """Test that HTML contains processed markdown content."""
        output_file = temp_output_dir / "test.html"
        convert_markdown_to_html(cursor_sample_md, output_file)
        html_content = output_file.read_text()
        # Should contain User/Cursor entries with IDs
        assert 'id="user-' in html_content or 'id="cursor-' in html_content
        # Should contain table of contents if entries exist
        assert "table-of-contents" in html_content

    def test_html_has_proper_structure(self, cursor_sample_md: Path, temp_output_dir: Path):
        """Test that generated HTML has proper document structure."""
        output_file = temp_output_dir / "test.html"
        convert_markdown_to_html(cursor_sample_md, output_file)
        html_content = output_file.read_text()
        assert "<!DOCTYPE html>" in html_content
        assert "<html" in html_content
        assert "<head>" in html_content
        assert "<body>" in html_content
        assert '<div class="container">' in html_content
