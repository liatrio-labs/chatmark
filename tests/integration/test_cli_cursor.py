"""Integration tests for CLI with Cursor markdown input."""

from pathlib import Path

import pytest

from chatmark.cli import app
from typer.testing import CliRunner

runner = CliRunner()


class TestCLICursor:
    """Integration tests for CLI with Cursor markdown format."""

    def test_cli_convert_cursor_to_html(self, cursor_sample_md: Path, temp_output_dir: Path):
        """Test CLI converts Cursor markdown to HTML."""
        output_file = temp_output_dir / "test.html"
        result = runner.invoke(
            app,
            [
                str(cursor_sample_md),
                "--format",
                "cursor-md",
                "--export",
                "html",
                "--output",
                str(output_file),
            ],
        )
        assert result.exit_code == 0
        assert output_file.exists()
        assert "Success" in result.stdout

    def test_cli_defaults_to_cursor_format(self, cursor_sample_md: Path, temp_output_dir: Path):
        """Test CLI defaults to cursor-md format."""
        output_file = temp_output_dir / "test.html"
        result = runner.invoke(
            app,
            [
                str(cursor_sample_md),
                "--export",
                "html",
                "--output",
                str(output_file),
            ],
        )
        assert result.exit_code == 0
        assert output_file.exists()

    def test_cli_defaults_to_html_export(self, cursor_sample_md: Path, temp_output_dir: Path):
        """Test CLI defaults to html export."""
        output_file = temp_output_dir / "test.html"
        result = runner.invoke(
            app,
            [
                str(cursor_sample_md),
                "--format",
                "cursor-md",
                "--output",
                str(output_file),
            ],
        )
        assert result.exit_code == 0
        assert output_file.exists()

    def test_cli_handles_nonexistent_file(self):
        """Test CLI handles nonexistent input file."""
        result = runner.invoke(
            app,
            [
                "/nonexistent/file.md",
                "--format",
                "cursor-md",
                "--export",
                "html",
            ],
        )
        assert result.exit_code == 1
        assert "not found" in result.stdout.lower()

