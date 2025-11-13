"""PDF exporter that converts internal markdown format to PDF using WeasyPrint."""

from pathlib import Path

from weasyprint import CSS as WeasyCSS
from weasyprint import HTML as WeasyHTML

from chatmark.core.converter import convert_markdown_to_html
from chatmark.exporters.base import BaseExporter

# PDF-specific CSS with fixes for page breaks and code wrapping
PDF_CSS = """
    /* Page setup - no margins */
    @page {
        size: A4;
        margin: 0mm;
        padding: 0mm;
    }

    /* Preserve dark theme colors */
    html {
        background-color: #111111 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    body {
        background-color: #111111 !important;
        margin: 0 !important;
        padding: 1cm !important;
        color: #ffffff !important;
        min-height: 100vh !important;
    }

    /* Container styling */
    .container {
        background-color: #111111 !important;
        margin: 0 !important;
        padding: 0 !important;
        max-width: none !important;
        width: 100% !important;
    }

    /* Preserve colors in PDF */
    * {
        -weasy-print-color-adjust: exact !important;
        color-adjust: exact !important;
        print-color-adjust: exact !important;
    }

    /* Improved page break handling - less intrusive */
    /* Only avoid breaks for very small elements */
    h1, h2, h3, h4, h5, h6 {
        page-break-inside: avoid;
        orphans: 3;
        widows: 3;
    }

    /* Allow natural breaks for larger blocks */
    p {
        page-break-inside: auto;
        orphans: 2;
        widows: 2;
    }

    /* Code blocks - allow wrapping and natural breaks */
    pre {
        background-color: #1e1e1e !important;
        color: #ffffff !important;
        border: 1px solid #3a3a3a !important;
        border-radius: 8px;
        padding: 1rem;
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        word-break: break-all !important;
        max-width: 100% !important;
        page-break-inside: auto;
        orphans: 2;
        widows: 2;
    }

    /* Inline code - wrap long strings */
    code {
        background-color: #1e1e1e !important;
        color: #89DF00 !important;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        border: 1px solid #3a3a3a;
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        word-break: break-all !important;
        max-width: 100% !important;
    }

    /* Pre code - ensure wrapping */
    pre code {
        background: none !important;
        border: none !important;
        padding: 0 !important;
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        word-break: break-all !important;
        max-width: 100% !important;
    }

    /* Tables - allow breaks but try to keep rows together */
    table {
        page-break-inside: auto;
        width: 100% !important;
        table-layout: fixed;
    }

    tr {
        page-break-inside: avoid;
    }

    /* Blockquotes - allow natural breaks */
    blockquote {
        page-break-inside: auto;
        orphans: 2;
        widows: 2;
    }

    /* Lists - allow breaks but keep items together */
    ul, ol {
        page-break-inside: auto;
    }

    li {
        page-break-inside: avoid;
        orphans: 2;
        widows: 2;
    }

    /* Links styling */
    a {
        color: #24AE1D !important;
    }

    /* Remove headers/footers */
    header, footer {
        display: none !important;
    }

    /* Ensure text wrapping for all text elements */
    p, div, span {
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }

    /* Table of contents - avoid breaking */
    .table-of-contents {
        page-break-inside: avoid;
    }

    /* Back to top links - avoid breaking */
    .back-to-top {
        page-break-inside: avoid;
    }
"""


class PDFExporter(BaseExporter):
    """Exporter that converts internal markdown format to PDF output.

    This exporter first converts markdown to HTML using the core converter,
    then uses WeasyPrint to generate PDF files with proper styling.
    """

    def export(self, content: str, output_path: str) -> str:
        """Export internal markdown format to PDF file.

        Args:
            content: Content in internal markdown format standard with **User** and **AI** markers.
            output_path: Path where the PDF file should be written.

        Returns:
            Path to the created PDF file.
        """
        # Convert markdown to HTML first
        temp_md = Path(output_path).with_suffix(".tmp.md")
        temp_html = Path(output_path).with_suffix(".tmp.html")
        temp_md.parent.mkdir(parents=True, exist_ok=True)
        temp_md.write_text(content, encoding="utf-8")

        # Convert markdown to HTML using core converter
        convert_markdown_to_html(temp_md, temp_html)

        # Read HTML content
        html_content = temp_html.read_text(encoding="utf-8")

        # Create HTML object
        html_doc = WeasyHTML(string=html_content, base_url=str(temp_html.parent))

        # Create CSS object
        css_doc = WeasyCSS(string=PDF_CSS)

        # Generate PDF
        pdf_path = Path(output_path)
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        html_doc.write_pdf(pdf_path, stylesheets=[css_doc])

        # Clean up temporary files
        temp_md.unlink()
        temp_html.unlink()

        return str(pdf_path)
