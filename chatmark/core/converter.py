"""Core conversion orchestration logic."""

import re
from datetime import datetime
from pathlib import Path

import markdown

from chatmark.core.html_generator import (
    add_back_to_top_links,
    add_heading_ids,
    add_user_cursor_ids,
    extract_headings,
    extract_user_cursor_entries_from_html,
    generate_html_document,
    generate_table_of_contents,
)


def convert_markdown_to_html(markdown_file: Path, output_file: Path | None = None) -> Path:
    """
    Convert a markdown file to HTML with Liatrio dark theme styling.

    Args:
        markdown_file: Path to input markdown file
        output_file: Optional path to output HTML file. If not provided,
                     uses the same name as input with timestamp suffix and .html extension.

    Returns:
        Path to the created HTML file
    """
    if not markdown_file.exists():
        raise FileNotFoundError(f"Markdown file not found: {markdown_file}")

    # Determine output file path
    if output_file is None:
        # Add timestamp suffix to filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = markdown_file.parent / f"{markdown_file.stem}_{timestamp}.html"

    # Read markdown content
    with open(markdown_file, encoding="utf-8") as f:
        markdown_content = f.read()

    # Configure markdown extensions
    md_extensions = [
        "fenced_code",
        "tables",
        "nl2br",
        "sane_lists",
        "toc",
    ]

    # Convert markdown to HTML
    md = markdown.Markdown(extensions=md_extensions)
    html_body = md.convert(markdown_content)

    # Add IDs to User/Cursor paragraphs
    html_body = add_user_cursor_ids(html_body)

    # Extract User/Cursor entries from HTML (after IDs are added)
    # This ensures we only include entries that actually have IDs
    user_cursor_entries = extract_user_cursor_entries_from_html(html_body)

    # Add IDs to headings for anchor links
    html_body = add_heading_ids(html_body)

    # Extract headings for table of contents
    headings = extract_headings(html_body)

    # Generate table of contents (with User/Cursor entries if present)
    toc_html = generate_table_of_contents(headings, user_cursor_entries)

    # Insert table of contents after the first h1 heading
    if toc_html:
        h1_pattern = re.compile(r"(<h1[^>]*>.*?</h1>)", re.DOTALL)

        def insert_toc(match: re.Match[str]) -> str:
            h1_tag = match.group(1)
            return f"{h1_tag}\n{toc_html}\n    <hr />"

        html_body = h1_pattern.sub(insert_toc, html_body, count=1)

    # Add "Back to TOC" links after h2 headings
    if toc_html:
        html_body = add_back_to_top_links(html_body)

    # Get title from first heading or filename
    title_match = re.search(r"<h1[^>]*>(.*?)</h1>", html_body, re.DOTALL)
    if title_match:
        title_text = re.sub(r"<[^>]+>", "", title_match.group(1))
        title = f"{title_text} - Liatrio Documentation"
    else:
        title = f"{markdown_file.stem} - Liatrio Documentation"

    # Generate complete HTML document
    html_document = generate_html_document(html_body, title)

    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Write HTML file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_document)

    return output_file

