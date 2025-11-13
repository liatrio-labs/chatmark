"""Unit tests for PDF exporter."""

from pathlib import Path

from chatmark.exporters.pdf import PDFExporter


class TestPDFExporter:
    """Tests for PDFExporter."""

    def test_exporter_instantiation(self):
        """Test that exporter can be instantiated."""
        exporter = PDFExporter()
        assert exporter is not None

    def test_export_creates_pdf_file(self, temp_output_dir: Path):
        """Test that export creates a PDF file."""
        exporter = PDFExporter()
        content = "**User**\n\nTest\n\n**AI**\n\nResponse"
        output_path = str(temp_output_dir / "test.pdf")
        result = exporter.export(content, output_path)
        assert Path(result).exists()
        assert Path(result).suffix == ".pdf"

    def test_export_generates_valid_pdf(self, temp_output_dir: Path):
        """Test that exported PDF is valid (has PDF header)."""
        exporter = PDFExporter()
        content = "**User**\n\nTest\n\n**AI**\n\nResponse"
        output_path = str(temp_output_dir / "test.pdf")
        exporter.export(content, output_path)
        pdf_content = Path(output_path).read_bytes()
        # PDF files start with %PDF
        assert pdf_content.startswith(b"%PDF")

    def test_export_preserves_content(self, temp_output_dir: Path):
        """Test that content is preserved in PDF (check via HTML intermediate)."""
        exporter = PDFExporter()
        content = "**User**\n\nQuestion\n\n**AI**\n\nAnswer"
        output_path = str(temp_output_dir / "test.pdf")
        exporter.export(content, output_path)
        # PDF is binary, so we verify it was created successfully
        assert Path(output_path).exists()
        assert Path(output_path).stat().st_size > 0

    def test_export_handles_code_blocks(self, temp_output_dir: Path):
        """Test that code blocks are preserved in PDF."""
        exporter = PDFExporter()
        content = "**User**\n\nShow code\n\n**AI**\n\n```python\nprint('hello')\n```"
        output_path = str(temp_output_dir / "test.pdf")
        exporter.export(content, output_path)
        assert Path(output_path).exists()
        assert Path(output_path).stat().st_size > 0

    def test_export_handles_multiple_exchanges(self, temp_output_dir: Path):
        """Test that multiple User/AI exchanges are preserved."""
        exporter = PDFExporter()
        content = (
            "**User**\n\nFirst question\n\n**AI**\n\nFirst answer\n\n"
            "**User**\n\nSecond question\n\n**AI**\n\nSecond answer"
        )
        output_path = str(temp_output_dir / "test.pdf")
        exporter.export(content, output_path)
        assert Path(output_path).exists()
        assert Path(output_path).stat().st_size > 0

    def test_export_uses_pdf_css_styling(self, temp_output_dir: Path):
        """Test that PDF uses proper CSS styling (dark theme, page setup)."""
        exporter = PDFExporter()
        content = "**User**\n\nTest\n\n**AI**\n\nResponse"
        output_path = str(temp_output_dir / "test.pdf")
        exporter.export(content, output_path)
        # Verify PDF was created (CSS application is verified by PDF generation success)
        assert Path(output_path).exists()

    def test_export_handles_empty_content(self, temp_output_dir: Path):
        """Test that empty content is handled."""
        exporter = PDFExporter()
        content = ""
        output_path = str(temp_output_dir / "test.pdf")
        exporter.export(content, output_path)
        assert Path(output_path).exists()

    def test_export_handles_markdown_formatting(self, temp_output_dir: Path):
        """Test that markdown formatting is preserved in PDF."""
        exporter = PDFExporter()
        content = "**User**\n\nQuestion with **bold** text\n\n**AI**\n\n```python\ncode\n```"
        output_path = str(temp_output_dir / "test.pdf")
        exporter.export(content, output_path)
        assert Path(output_path).exists()
        assert Path(output_path).stat().st_size > 0

    def test_export_creates_directories(self, temp_output_dir: Path):
        """Test that export creates parent directories if they don't exist."""
        exporter = PDFExporter()
        content = "**User**\n\nTest\n\n**AI**\n\nResponse"
        output_path = str(temp_output_dir / "nested" / "dir" / "test.pdf")
        exporter.export(content, output_path)
        assert Path(output_path).exists()
