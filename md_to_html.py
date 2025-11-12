#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "markdown>=3.5",
#   "typer>=0.12",
#   "rich>=13.0",
#   "weasyprint>=62.0",
# ]
# ///

"""
Convert markdown files to HTML with Liatrio dark theme styling.

This script converts markdown files to beautifully styled HTML using
Liatrio's dark theme brand colors and styling. When no output file is
specified, a timestamp suffix is automatically added to the filename.
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.text import Text

try:
    import markdown
except ImportError:
    console = Console(stderr=True)
    console.print("[bold red]Error:[/] markdown library not found. Install with: [cyan]uv add --script md_to_html.py markdown[/]")
    raise typer.Exit(1)

try:
    from weasyprint import HTML as WeasyHTML, CSS as WeasyCSS
    from weasyprint.text.fonts import FontConfiguration
except ImportError:
    weasyprint_available = False
else:
    weasyprint_available = True

# Initialize Rich console
console = Console()


# Liatrio Dark Theme CSS
LIATRIO_CSS = """        :root {
            /* Liatrio Brand Colors - Dark Theme */
            --bg-primary: #111111;
            --bg-secondary: #1e1e1e;
            --bg-tertiary: #3a3a3a;
            --text-primary: #ffffff;
            --text-secondary: #eeeeee;
            --text-muted: #9c9c9c;
            --accent-primary: #24AE1D;
            --accent-secondary: #89DF00;
            --accent-lagoon: #00C1DB;
            --accent-deep-sea: #007DAA;
            --accent-hot-red: #FF5100;
            --accent-flame: #FFAA00;
            --border-color: #444444;
            --code-bg: #1e1e1e;
            --code-border: #3a3a3a;
        }

        * {
            box-sizing: border-box;
        }

        body {
            font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            margin: 0;
            padding: 0;
            font-size: 16px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }

        /* Typography */
        h1,
        h2,
        h3,
        h4,
        h5,
        h6 {
            font-family: 'Clash Display', 'Anybody', 'DM Sans', sans-serif;
            font-weight: 700;
            color: var(--text-primary);
            margin-top: 2rem;
            margin-bottom: 1rem;
            line-height: 1.2;
        }

        h1 {
            font-size: 2.5rem;
            border-bottom: 3px solid var(--accent-primary);
            padding-bottom: 0.5rem;
        }

        h2 {
            font-size: 2rem;
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 0.3rem;
        }

        h3 {
            font-size: 1.5rem;
            color: var(--accent-secondary);
        }

        h4 {
            font-size: 1.25rem;
            color: var(--accent-lagoon);
        }

        p {
            margin-bottom: 1rem;
            color: var(--text-secondary);
        }

        /* Links */
        a {
            color: var(--accent-primary);
            text-decoration: none;
            transition: color 0.2s ease;
        }

        a:hover {
            color: var(--accent-secondary);
            text-decoration: underline;
        }

        /* Lists */
        ul,
        ol {
            margin-bottom: 1rem;
            padding-left: 2rem;
        }

        li {
            margin-bottom: 0.5rem;
            color: var(--text-secondary);
        }

        /* Code */
        code {
            background-color: var(--code-bg);
            color: var(--accent-secondary);
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 0.9em;
            border: 1px solid var(--code-border);
            white-space: pre-wrap;
            word-wrap: break-word;
            overflow-wrap: break-word;
            word-break: break-all;
            max-width: 100%;
        }

        pre {
            background-color: var(--code-bg);
            border: 1px solid var(--code-border);
            border-radius: 8px;
            padding: 1rem;
            overflow-x: auto;
            overflow-wrap: break-word;
            word-wrap: break-word;
            white-space: pre-wrap;
            word-break: break-all;
            margin-bottom: 1rem;
            max-width: 100%;
        }

        pre code {
            background: none;
            border: none;
            padding: 0;
            color: var(--text-primary);
            white-space: pre-wrap;
            word-wrap: break-word;
            overflow-wrap: break-word;
            word-break: break-all;
            max-width: 100%;
        }

        /* Blockquotes */
        blockquote {
            border-left: 4px solid var(--accent-primary);
            margin: 1rem 0;
            padding: 0.5rem 1rem;
            background-color: var(--bg-secondary);
            color: var(--text-muted);
        }

        /* Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 1rem;
            background-color: var(--bg-secondary);
        }

        th,
        td {
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }

        th {
            background-color: var(--bg-tertiary);
            color: var(--text-primary);
            font-weight: 600;
        }

        td {
            color: var(--text-secondary);
        }

        tr:hover {
            background-color: var(--bg-tertiary);
        }

        /* Horizontal Rule */
        hr {
            border: none;
            height: 2px;
            background: linear-gradient(to right, var(--accent-primary), var(--accent-lagoon));
            margin: 2rem 0;
        }

        /* Status Indicators */
        .status-pass {
            color: var(--accent-primary);
            font-weight: 600;
        }

        .status-fail {
            color: var(--accent-hot-red);
            font-weight: 600;
        }

        .status-warning {
            color: var(--accent-flame);
            font-weight: 600;
        }

        /* Proof artifacts and code references */
        .code-ref {
            background-color: var(--bg-tertiary);
            padding: 0.1rem 0.3rem;
            border-radius: 3px;
            font-family: monospace;
            font-size: 0.85em;
        }

        /* Section styling */
        .executive-summary {
            background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
            padding: 1.5rem;
            border-radius: 8px;
            margin-bottom: 2rem;
            border-left: 5px solid var(--accent-primary);
        }

        /* Metrics styling */
        .metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }

        .metric-card {
            background-color: var(--bg-secondary);
            padding: 1rem;
            border-radius: 6px;
            border: 1px solid var(--border-color);
        }

        /* Strong text styling */
        strong {
            color: var(--accent-primary);
            font-weight: 600;
        }

        /* Table of Contents */
        .table-of-contents {
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1.5rem;
            margin: 2rem 0;
        }

        .table-of-contents h2 {
            margin-top: 0;
            color: var(--accent-primary);
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.5rem;
        }

        .toc-list {
            list-style: none;
            padding-left: 0;
            margin: 0;
        }

        .toc-list ul {
            list-style: none;
            padding-left: 0;
            margin: 0.25rem 0 0.25rem 1.5rem;
            border-left: 2px solid var(--border-color);
            position: relative;
        }

        .toc-list ul::before {
            content: '';
            position: absolute;
            left: -2px;
            top: 0;
            bottom: 0;
            width: 2px;
            background-color: var(--bg-secondary);
        }

        .toc-list li {
            margin-bottom: 0.25rem;
            padding: 0;
            position: relative;
            line-height: 1.6;
        }

        .toc-list li::before {
            content: '├─';
            position: absolute;
            left: -1.5rem;
            color: var(--accent-lagoon);
            font-weight: normal;
        }

        .toc-list > li::before {
            display: none;
        }

        .toc-list ul > li:last-child::before {
            content: '└─';
        }

        .toc-list a {
            color: var(--text-secondary);
            text-decoration: none;
            transition: all 0.2s ease;
            display: inline-block;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            margin-left: 0;
        }

        .toc-list a:hover {
            color: var(--accent-primary);
            background-color: var(--bg-tertiary);
            text-decoration: none;
        }

        /* User/Cursor ToC entries */
        .toc-legend {
            margin: 1rem 0;
            font-size: 0.9rem;
            text-align: center;
        }

        .legend-user {
            color: var(--accent-lagoon);
            font-weight: 600;
            margin-right: 1rem;
        }

        .legend-cursor {
            color: var(--accent-secondary);
            font-weight: 600;
        }

        .user-entry {
            border-radius: 8px;
            transition: all 0.2s ease;
        }

        .user-entry .toc-link {
            border-radius: 8px;
        }

        .user-entry .toc-link:hover {
            background-color: rgba(0, 193, 219, 0.1);
            transform: translateX(4px);
        }

        .cursor-entry {
            margin-bottom: 0.75rem;
            border-radius: 8px;
            transition: all 0.2s ease;
        }

        .cursor-entry .toc-link {
            border-radius: 8px;
        }

        .cursor-entry .toc-link:hover {
            background-color: rgba(137, 223, 0, 0.1);
            transform: translateX(4px);
        }

        .toc-link {
            text-decoration: none;
            font-weight: 600;
            display: block;
            padding: 0.75rem;
            transition: color 0.2s ease, background-color 0.2s ease, transform 0.2s ease;
        }

        .toc-user {
            color: var(--text-secondary);
        }

        .toc-user:hover {
            color: var(--accent-lagoon);
            text-decoration: underline;
        }

        .toc-cursor {
            color: var(--text-secondary);
        }

        .toc-cursor:hover {
            color: var(--accent-secondary);
            text-decoration: underline;
        }

        .speaker-label {
            font-weight: 700;
            display: inline-block;
            min-width: 80px;
            padding: 0.2rem 0.6rem;
            border-radius: 4px;
            margin-right: 0.5rem;
            font-size: 0.85em;
        }

        .toc-user .speaker-label {
            background-color: rgba(0, 193, 219, 0.2);
            color: var(--accent-lagoon);
            border: 1px solid var(--accent-lagoon);
        }

        .toc-cursor .speaker-label {
            background-color: rgba(137, 223, 0, 0.2);
            color: var(--accent-secondary);
            border: 1px solid var(--accent-secondary);
        }

        .toc-divider {
            color: var(--accent-lagoon);
            margin: 0 0.4rem;
            font-weight: 600;
            font-size: 1.1em;
            display: inline-block;
            text-decoration: none !important;
        }

        .cursor-entry .toc-divider {
            color: var(--accent-secondary);
        }

        .toc-link:hover .toc-divider {
            text-decoration: none !important;
        }

        .preview-text {
            font-weight: normal;
            font-style: italic;
            color: var(--text-muted);
            background-color: rgba(0, 193, 219, 0.1);
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            display: inline-block;
        }

        .cursor-entry .preview-text {
            background-color: rgba(137, 223, 0, 0.1);
        }

        .back-to-top {
            text-align: right;
            margin: -0.5rem 0 1rem 0;
            font-size: 0.85rem;
        }

        .back-to-top a {
            color: var(--text-muted);
            text-decoration: none;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            background-color: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            transition: all 0.2s ease;
        }

        .back-to-top a:hover {
            color: var(--accent-primary);
            background-color: var(--border-color);
            text-decoration: none;
        }

        /* Responsive design */
        @media (max-width: 768px) {
            .container {
                padding: 1rem;
            }

            h1 {
                font-size: 2rem;
            }

            h2 {
                font-size: 1.5rem;
            }
        }"""


def slugify(text):
    """Convert text to a URL-friendly slug."""
    # Convert to lowercase and replace spaces/special chars with hyphens
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def add_heading_ids(html_content):
    """Add ID attributes to headings for anchor links."""
    # Pattern to match headings
    heading_pattern = re.compile(r'<h([1-6])>(.*?)</h\1>', re.DOTALL)
    
    def add_id(match):
        level = match.group(1)
        content = match.group(2)
        # Extract text content (remove any HTML tags)
        text_content = re.sub(r'<[^>]+>', '', content)
        heading_id = slugify(text_content)
        return f'<h{level} id="{heading_id}">{content}</h{level}>'
    
    return heading_pattern.sub(add_id, html_content)


def extract_user_cursor_entries_from_html(html_content):
    """Extract User and Cursor entries from HTML content that have IDs."""
    entries = []
    # Pattern to match <p id="user-X"> or <p id="cursor-X">
    pattern = re.compile(r'<p id="(user|cursor)-(\d+)"><strong>(User|Cursor)</strong></p>', re.IGNORECASE)
    
    for match in pattern.finditer(html_content):
        speaker_type = match.group(3)  # "User" or "Cursor"
        entry_num = int(match.group(2))
        
        # Get preview text from next non-empty paragraph (up to 100 chars)
        # Find the position after this match
        start_pos = match.end()
        # Look for the next <p> tag that's not empty
        next_p_match = re.search(r'<p[^>]*>(.*?)</p>', html_content[start_pos:start_pos+500], re.DOTALL)
        
        preview_text = ""
        if next_p_match:
            preview_text = re.sub(r'<[^>]+>', '', next_p_match.group(1)).strip()
            # Remove any HTML entities and clean up
            preview_text = preview_text.replace('<br />', ' ').replace('\n', ' ')
            preview_text = ' '.join(preview_text.split())
            if len(preview_text) > 100:
                preview_text = preview_text[:97] + '...'
        
        entry_id = f"{speaker_type.lower()}-{entry_num}"
        entries.append({
            'type': speaker_type,
            'id': entry_id,
            'number': entry_num,
            'preview': preview_text
        })
    
    return entries


def add_user_cursor_ids(html_content):
    """Add IDs to User and Cursor paragraphs in HTML."""
    # Pattern to match <p><strong>User</strong></p> or <p><strong>Cursor</strong></p>
    pattern = re.compile(r'(<p><strong>(User|Cursor)</strong></p>)', re.IGNORECASE)
    
    entry_num = {'User': 0, 'Cursor': 0}
    
    def add_id(match):
        speaker = match.group(2)
        entry_num[speaker] += 1
        entry_id = f"{speaker.lower()}-{entry_num[speaker]}"
        return f'<p id="{entry_id}"><strong>{speaker}</strong></p>'
    
    return pattern.sub(add_id, html_content)


def extract_headings(html_content):
    """Extract all headings from HTML content and return list of (level, id, text) tuples."""
    headings = []
    heading_pattern = re.compile(r'<h([1-6]) id="([^"]+)">(.*?)</h\1>', re.DOTALL)
    
    for match in heading_pattern.finditer(html_content):
        level = int(match.group(1))
        heading_id = match.group(2)
        content = match.group(3)
        # Extract text content (remove any HTML tags)
        text_content = re.sub(r'<[^>]+>', '', content).strip()
        headings.append((level, heading_id, text_content))
    
    return headings


def generate_table_of_contents(headings, user_cursor_entries=None):
    """Generate HTML for table of contents from headings list as a nested tree structure.
    
    Args:
        headings: List of (level, id, text) tuples for headings
        user_cursor_entries: Optional list of User/Cursor entry dicts
    """
    has_user_cursor = user_cursor_entries and len(user_cursor_entries) > 0
    
    # If we have User/Cursor entries, use them instead of headings
    if has_user_cursor:
        toc_items = []
        for entry in user_cursor_entries:
            entry_type = entry['type']
            entry_id = entry['id']
            entry_num = entry['number']
            preview = entry['preview']
            
            css_class = 'user-entry' if entry_type == 'User' else 'cursor-entry'
            link_class = 'toc-link toc-user' if entry_type == 'User' else 'toc-link toc-cursor'
            
            toc_items.append(
                f'        <li class="{css_class}">'
                f'<a href="#{entry_id}" class="{link_class}">'
                f'<span class="speaker-label">{entry_type} {entry_num}</span>'
                f'<span class="toc-divider">❱</span>'
                f'<span class="preview-text">{preview}</span></a></li>'
            )
        
        toc_html = f"""    <div class="table-of-contents">
        <h2 id="table-of-contents">Table of Contents</h2>
        <ul class="toc-list">
{chr(10).join(toc_items)}
        </ul>
    </div>"""
        
        return toc_html
    
    # Otherwise, use headings tree structure
    if not headings:
        return ""
    
    # Filter out the first h1 (document title)
    filtered_headings = []
    first_heading_skipped = False
    
    for level, heading_id, text in headings:
        # Skip the first h1 if it's the document title
        if level == 1 and not first_heading_skipped:
            first_heading_skipped = True
            continue
        filtered_headings.append((level, heading_id, text))
    
    if not filtered_headings:
        return ""
    
    # Build nested tree structure
    def build_tree(items, start_idx=0, current_level=2, indent=8):
        """Recursively build nested list structure."""
        html_parts = []
        i = start_idx
        indent_str = ' ' * indent
        
        while i < len(items):
            level, heading_id, text = items[i]
            
            # If we've gone back to a higher level, we're done with this branch
            if level < current_level:
                break
            
            # If this is at our current level, add it
            if level == current_level:
                html_parts.append(f'{indent_str}<li><a href="#{heading_id}">{text}</a>')
                i += 1
                
                # Check if next items are children
                if i < len(items) and items[i][0] > current_level:
                    # Recursively add children
                    child_html, new_idx = build_tree(items, i, current_level + 1, indent + 4)
                    html_parts.append(child_html)
                    i = new_idx
                
                html_parts.append(f'{indent_str}</li>')
            else:
                # This shouldn't happen if structure is correct, but handle it
                break
        
        tree_html = '\n'.join(html_parts)
        if tree_html.strip():
            return f'{indent_str}<ul>\n{tree_html}\n{indent_str}</ul>', i
        return '', i
    
    tree_html, _ = build_tree(filtered_headings)
    
    if not tree_html:
        return ""
    
    # Remove the outer <ul> wrapper since we already have .toc-list
    tree_html = tree_html.strip()
    if tree_html.startswith('<ul>') and tree_html.endswith('</ul>'):
        # Extract content between <ul> tags
        tree_html = tree_html[4:-5].strip()
    
    toc_html = f"""    <div class="table-of-contents">
        <h2 id="table-of-contents">Table of Contents</h2>
        <ul class="toc-list">
{tree_html}
        </ul>
    </div>"""
    
    return toc_html


def add_back_to_top_links(html_content):
    """Add 'Back to TOC' links after h2 headings and User/Cursor entries, excluding the Table of Contents heading."""
    # Pattern to match h2 headings, but exclude the table-of-contents one
    h2_pattern = re.compile(r'(<h2 id="table-of-contents">.*?</h2>)|(<h2[^>]*>.*?</h2>)', re.DOTALL)
    
    def add_back_link_h2(match):
        h2_tag = match.group(0)
        # Skip if this is the table-of-contents heading
        if 'id="table-of-contents"' in h2_tag:
            return h2_tag
        return f'{h2_tag}\n    <div class="back-to-top"><a href="#table-of-contents">↑ Back to TOC</a></div>'
    
    html_content = h2_pattern.sub(add_back_link_h2, html_content)
    
    # Pattern to match User/Cursor paragraphs with IDs
    user_cursor_pattern = re.compile(r'(<p id="(user|cursor)-\d+"><strong>(User|Cursor)</strong></p>)', re.IGNORECASE)
    
    def add_back_link_user_cursor(match):
        p_tag = match.group(0)
        return f'{p_tag}\n    <div class="back-to-top"><a href="#table-of-contents">↑ Back to TOC</a></div>'
    
    html_content = user_cursor_pattern.sub(add_back_link_user_cursor, html_content)
    
    return html_content


def convert_markdown_to_html(markdown_file: Path, output_file: Path = None) -> Path:
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
    with open(markdown_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Extract User/Cursor entries before conversion (for initial processing)
    # We'll re-extract from HTML after IDs are added to ensure accuracy
    
    # Configure markdown extensions
    md_extensions = [
        'fenced_code',
        'tables',
        'nl2br',
        'sane_lists',
        'toc',
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
        h1_pattern = re.compile(r'(<h1[^>]*>.*?</h1>)', re.DOTALL)
        def insert_toc(match):
            h1_tag = match.group(1)
            return f'{h1_tag}\n{toc_html}\n    <hr />'
        html_body = h1_pattern.sub(insert_toc, html_body, count=1)
    
    # Add "Back to TOC" links after h2 headings
    if toc_html:
        html_body = add_back_to_top_links(html_body)
    
    # Get title from first heading or filename
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html_body, re.DOTALL)
    if title_match:
        title_text = re.sub(r'<[^>]+>', '', title_match.group(1))
        title = f"{title_text} - Liatrio Documentation"
    else:
        title = f"{markdown_file.stem} - Liatrio Documentation"
    
    # Build complete HTML document
    html_document = f"""<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
{LIATRIO_CSS}
    </style>
</head>

<body>
    <div class="container">
{html_body}
    </div>
</body>

</html>"""
    
    # Write HTML file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_document)
    
    return output_file


def convert_html_to_pdf(html_file: Path, pdf_file: Path) -> Path:
    """
    Convert HTML file to PDF using WeasyPrint with improved styling.
    
    Args:
        html_file: Path to input HTML file
        pdf_file: Path to output PDF file
    
    Returns:
        Path to the created PDF file
    """
    if not weasyprint_available:
        raise ImportError("WeasyPrint is not available. Install with: uv add --script md_to_html.py weasyprint")
    
    if not html_file.exists():
        raise FileNotFoundError(f"HTML file not found: {html_file}")
    
    # Read HTML content
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # PDF-specific CSS with fixes for page breaks and code wrapping
    pdf_css = """
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
    
    # Create HTML object
    html_doc = WeasyHTML(string=html_content, base_url=str(html_file.parent))
    
    # Create CSS object
    css_doc = WeasyCSS(string=pdf_css)
    
    # Generate PDF
    font_config = FontConfiguration()
    html_doc.write_pdf(
        pdf_file,
        stylesheets=[css_doc],
        font_config=font_config,
        optimize_size=('fonts', 'images')
    )
    
    return pdf_file
app = typer.Typer(
    name="md_to_html",
    help="Convert markdown files to HTML with Liatrio dark theme styling.",
    add_completion=False,
)


@app.command()
def main(
    input_file: Annotated[
        Path,
        typer.Argument(
            help="Path to the input markdown file to convert.",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
        ),
    ],
    output_file: Annotated[
        Optional[Path],
        typer.Option(
            "--output",
            "-o",
            help="Path to the output HTML file. If not provided, uses the input filename with timestamp suffix.",
            file_okay=True,
            dir_okay=False,
            writable=True,
        ),
    ] = None,
    pdf: Annotated[
        bool,
        typer.Option(
            "--pdf",
            help="Also generate a PDF version of the HTML output.",
        ),
    ] = False,
) -> None:
    """
    Convert markdown files to HTML with Liatrio dark theme styling.

    Features:
    - Automatic table of contents generation with tree structure
    - Support for User/Cursor conversation entries in ToC
    - Timestamp suffix for auto-generated output filenames
    - Responsive design with Liatrio brand colors
    - Anchor links and "Back to TOC" navigation
    - Optional PDF generation with improved page breaks and code wrapping

    Examples:
        # Convert with auto-generated timestamp filename
        md_to_html.py document.md

        # Convert with custom output filename
        md_to_html.py document.md --output output.html
        md_to_html.py document.md -o output.html

        # Convert and also generate PDF
        md_to_html.py document.md --pdf
        md_to_html.py document.md -o output.html --pdf
    """
    try:
        # Show status while converting
        with console.status("[bold cyan]Converting markdown to HTML...", spinner="dots"):
            output_path = convert_markdown_to_html(input_file, output_file)
        
        # Success message with Rich formatting
        success_text = Text()
        success_text.append("✅ ", style="bold green")
        success_text.append("Successfully converted: ", style="green")
        success_text.append(str(input_file), style="cyan")
        success_text.append(" → ", style="dim")
        success_text.append(str(output_path), style="bold cyan")
        
        console.print(success_text)
        
        # Show file size if output file exists
        if output_path.exists():
            size = output_path.stat().st_size
            if size >= 1024 * 1024:
                size_str = f"{size / (1024 * 1024):.1f} MB"
            elif size >= 1024:
                size_str = f"{size / 1024:.0f} KB"
            else:
                size_str = f"{size} B"
            
            console.print(f"[dim]Output size: {size_str}[/]")
        
        # Generate PDF if requested
        if pdf:
            if not weasyprint_available:
                console.print("[bold yellow]Warning:[/] WeasyPrint not available. Skipping PDF generation.", style="yellow")
                console.print("[dim]Install with: uv add --script md_to_html.py weasyprint[/]")
            else:
                pdf_output = output_path.with_suffix('.pdf')
                with console.status("[bold cyan]Generating PDF...", spinner="dots"):
                    pdf_path = convert_html_to_pdf(output_path, pdf_output)
                
                pdf_success_text = Text()
                pdf_success_text.append("✅ ", style="bold green")
                pdf_success_text.append("PDF generated: ", style="green")
                pdf_success_text.append(str(pdf_path), style="bold cyan")
                console.print(pdf_success_text)
                
                if pdf_path.exists():
                    pdf_size = pdf_path.stat().st_size
                    if pdf_size >= 1024 * 1024:
                        pdf_size_str = f"{pdf_size / (1024 * 1024):.1f} MB"
                    elif pdf_size >= 1024:
                        pdf_size_str = f"{pdf_size / 1024:.0f} KB"
                    else:
                        pdf_size_str = f"{pdf_size} B"
                    
                    console.print(f"[dim]PDF size: {pdf_size_str}[/]")
        
    except FileNotFoundError as e:
        error_text = Text()
        error_text.append("❌ ", style="bold red")
        error_text.append("Error: ", style="red")
        error_text.append(str(e), style="white")
        console.print(error_text, style="red")
        raise typer.Exit(1)
    except Exception as e:
        error_text = Text()
        error_text.append("❌ ", style="bold red")
        error_text.append(f"Error converting {input_file}: ", style="red")
        error_text.append(str(e), style="white")
        console.print(error_text, style="red")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()

