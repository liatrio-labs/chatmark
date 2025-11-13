"""Integration tests for CLI with all export formats."""

from pathlib import Path

from typer.testing import CliRunner

from chatmark.cli import app

runner = CliRunner()


class TestCLIExports:
    """Integration tests for CLI with all export format combinations."""

    def test_cursor_to_markdown(self, cursor_sample_md: Path, temp_output_dir: Path):
        """Test CLI converts Cursor markdown to markdown."""
        output_file = temp_output_dir / "test.md"
        result = runner.invoke(
            app,
            [
                str(cursor_sample_md),
                "--format",
                "cursor-md",
                "--export",
                "markdown",
                "--output",
                str(output_file),
            ],
        )
        assert result.exit_code == 0
        assert output_file.exists()
        assert "Success" in result.stdout

    def test_cursor_to_html(self, cursor_sample_md: Path, temp_output_dir: Path):
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

    def test_cursor_to_pdf(self, cursor_sample_md: Path, temp_output_dir: Path):
        """Test CLI converts Cursor markdown to PDF."""
        output_file = temp_output_dir / "test.pdf"
        result = runner.invoke(
            app,
            [
                str(cursor_sample_md),
                "--format",
                "cursor-md",
                "--export",
                "pdf",
                "--output",
                str(output_file),
            ],
        )
        assert result.exit_code == 0
        assert output_file.exists()
        assert "Success" in result.stdout
        # Verify PDF is valid
        pdf_content = output_file.read_bytes()
        assert pdf_content.startswith(b"%PDF")

    def test_vscode_to_markdown(self, temp_output_dir: Path):
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

    def test_vscode_to_html(self, temp_output_dir: Path):
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

    def test_vscode_to_pdf(self, temp_output_dir: Path):
        """Test CLI converts VS Code JSON to PDF."""
        vscode_sample = Path(__file__).parent.parent / "fixtures" / "vscode_sample.json"
        output_file = temp_output_dir / "test.pdf"
        result = runner.invoke(
            app,
            [
                str(vscode_sample),
                "--format",
                "vscode",
                "--export",
                "pdf",
                "--output",
                str(output_file),
            ],
        )
        assert result.exit_code == 0
        assert output_file.exists()
        assert "Success" in result.stdout
        # Verify PDF is valid
        pdf_content = output_file.read_bytes()
        assert pdf_content.startswith(b"%PDF")

    def test_all_export_formats_from_cursor(self, cursor_sample_md: Path, temp_output_dir: Path):
        """Test all export formats work with Cursor markdown input."""
        formats = ["markdown", "html", "pdf"]
        for export_format in formats:
            output_file = temp_output_dir / f"test.{export_format if export_format != 'markdown' else 'md'}"
            result = runner.invoke(
                app,
                [
                    str(cursor_sample_md),
                    "--format",
                    "cursor-md",
                    "--export",
                    export_format,
                    "--output",
                    str(output_file),
                ],
            )
            assert result.exit_code == 0, f"Failed for export format: {export_format}"
            assert output_file.exists(), f"Output file not created for: {export_format}"

    def test_all_export_formats_from_vscode(self, temp_output_dir: Path):
        """Test all export formats work with VS Code JSON input."""
        vscode_sample = Path(__file__).parent.parent / "fixtures" / "vscode_sample.json"
        formats = ["markdown", "html", "pdf"]
        for export_format in formats:
            output_file = temp_output_dir / f"test.{export_format if export_format != 'markdown' else 'md'}"
            result = runner.invoke(
                app,
                [
                    str(vscode_sample),
                    "--format",
                    "vscode",
                    "--export",
                    export_format,
                    "--output",
                    str(output_file),
                ],
            )
            assert result.exit_code == 0, f"Failed for export format: {export_format}"
            assert output_file.exists(), f"Output file not created for: {export_format}"

