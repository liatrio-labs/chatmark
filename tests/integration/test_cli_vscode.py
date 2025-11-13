"""Integration tests for CLI with VS Code JSON input."""

from pathlib import Path

from typer.testing import CliRunner

from chatmark.cli import app

runner = CliRunner()


class TestCLIVSCode:
    """Integration tests for CLI with VS Code JSON format."""

    def test_cli_convert_vscode_to_markdown(self, temp_output_dir: Path):
        """Test CLI converts VS Code JSON to markdown."""
        vscode_sample = Path(__file__).parent.parent / "fixtures" / "vscode_sample.json"
        output_file = temp_output_dir / "test.md"
        result = runner.invoke(
            app,
            [
                str(vscode_sample),
                "--format",
                "vscode",
                "--export",
                "markdown",
                "--output",
                str(output_file),
            ],
        )
        assert result.exit_code == 0
        assert output_file.exists()
        assert "Success" in result.stdout

        # Verify output contains internal format markers
        content = output_file.read_text()
        assert "**User**" in content
        assert "**AI**" in content

    def test_cli_convert_vscode_to_html(self, temp_output_dir: Path):
        """Test CLI converts VS Code JSON to HTML."""
        vscode_sample = Path(__file__).parent.parent / "fixtures" / "vscode_sample.json"
        output_file = temp_output_dir / "test.html"
        result = runner.invoke(
            app,
            [
                str(vscode_sample),
                "--format",
                "vscode",
                "--export",
                "html",
                "--output",
                str(output_file),
            ],
        )
        assert result.exit_code == 0
        assert output_file.exists()
        assert "Success" in result.stdout

        # Verify HTML content
        html_content = output_file.read_text()
        assert "<!DOCTYPE html>" in html_content
        assert "**User**" in html_content or "<strong>User</strong>" in html_content

    def test_cli_handles_invalid_vscode_json(self, temp_output_dir: Path):
        """Test CLI handles invalid VS Code JSON gracefully."""
        temp_output_dir.mkdir(parents=True, exist_ok=True)
        invalid_json = temp_output_dir / "invalid.json"
        invalid_json.write_text('{"invalid": "structure"}')
        output_file = temp_output_dir / "test.md"
        result = runner.invoke(
            app,
            [
                str(invalid_json),
                "--format",
                "vscode",
                "--export",
                "markdown",
                "--output",
                str(output_file),
            ],
        )
        # Should handle gracefully (empty output or error)
        assert result.exit_code in (0, 1)

    def test_cli_vscode_output_conforms_to_internal_format(self, temp_output_dir: Path):
        """Test that VS Code conversion produces internal markdown format standard."""
        vscode_sample = Path(__file__).parent.parent / "fixtures" / "vscode_sample.json"
        output_file = temp_output_dir / "test.md"
        result = runner.invoke(
            app,
            [
                str(vscode_sample),
                "--format",
                "vscode",
                "--export",
                "markdown",
                "--output",
                str(output_file),
            ],
        )
        assert result.exit_code == 0

        content = output_file.read_text()
        # Should have proper format: **User**\n\n<text>\n\n**AI**\n\n<text>
        lines = content.split("\n")
        assert "**User**" in lines
        assert "**AI**" in lines
        # Verify structure
        assert content.count("**User**") == content.count("**AI**")
