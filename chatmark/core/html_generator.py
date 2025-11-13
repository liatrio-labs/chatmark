"""HTML generation utilities for converting markdown to styled HTML."""

import re

from chatmark.core.styles import LIATRIO_CSS


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    # Convert to lowercase and replace spaces/special chars with hyphens
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text.strip("-")


def add_heading_ids(html_content: str) -> str:
    """Add ID attributes to headings for anchor links."""
    # Pattern to match headings
    heading_pattern = re.compile(r"<h([1-6])>(.*?)</h\1>", re.DOTALL)

    def add_id(match: re.Match[str]) -> str:
        level = match.group(1)
        content = match.group(2)
        # Extract text content (remove any HTML tags)
        text_content = re.sub(r"<[^>]+>", "", content)
        heading_id = slugify(text_content)
        return f'<h{level} id="{heading_id}">{content}</h{level}>'

    return heading_pattern.sub(add_id, html_content)


def extract_user_cursor_entries_from_html(html_content: str) -> list[dict[str, str | int]]:
    """Extract User and Cursor entries from HTML content that have IDs."""
    entries = []
    # Pattern to match <p id="user-X"> or <p id="cursor-X">
    pattern = re.compile(
        r'<p id="(user|cursor)-(\d+)"><strong>(User|Cursor)</strong></p>', re.IGNORECASE
    )

    for match in pattern.finditer(html_content):
        speaker_type = match.group(3)  # "User" or "Cursor"
        entry_num = int(match.group(2))

        # Get preview text from next non-empty paragraph (up to 100 chars)
        # Find the position after this match
        start_pos = match.end()
        # Look for the next <p> tag that's not empty
        next_p_match = re.search(
            r"<p[^>]*>(.*?)</p>", html_content[start_pos : start_pos + 500], re.DOTALL
        )

        preview_text = ""
        if next_p_match:
            preview_text = re.sub(r"<[^>]+>", "", next_p_match.group(1)).strip()
            # Remove any HTML entities and clean up
            preview_text = preview_text.replace("<br />", " ").replace("\n", " ")
            preview_text = " ".join(preview_text.split())
            if len(preview_text) > 100:
                preview_text = preview_text[:97] + "..."

        entry_id = f"{speaker_type.lower()}-{entry_num}"
        entries.append(
            {"type": speaker_type, "id": entry_id, "number": entry_num, "preview": preview_text}
        )

    return entries


def add_user_cursor_ids(html_content: str) -> str:
    """Add IDs to User and Cursor paragraphs in HTML."""
    # Pattern to match <p><strong>User</strong></p> or <p><strong>Cursor</strong></p>
    pattern = re.compile(r"(<p><strong>(User|Cursor)</strong></p>)", re.IGNORECASE)

    entry_num = {"User": 0, "Cursor": 0}

    def add_id(match: re.Match[str]) -> str:
        speaker_match = match.group(2)
        # Normalize to capitalized form for dictionary key
        speaker = "User" if speaker_match.lower() == "user" else "Cursor"
        entry_num[speaker] += 1
        entry_id = f"{speaker.lower()}-{entry_num[speaker]}"
        return f'<p id="{entry_id}"><strong>{speaker}</strong></p>'

    return pattern.sub(add_id, html_content)


def extract_headings(html_content: str) -> list[tuple[int, str, str]]:
    """Extract all headings from HTML content and return list of (level, id, text) tuples."""
    headings = []
    heading_pattern = re.compile(r'<h([1-6]) id="([^"]+)">(.*?)</h\1>', re.DOTALL)

    for match in heading_pattern.finditer(html_content):
        level = int(match.group(1))
        heading_id = match.group(2)
        content = match.group(3)
        # Extract text content (remove any HTML tags)
        text_content = re.sub(r"<[^>]+>", "", content).strip()
        headings.append((level, heading_id, text_content))

    return headings


def generate_table_of_contents(
    headings: list[tuple[int, str, str]], user_cursor_entries: list[dict[str, str | int]] | None = None
) -> str:
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
            entry_type = str(entry["type"])
            entry_id = str(entry["id"])
            entry_num = int(entry["number"])
            preview = str(entry["preview"])

            css_class = "user-entry" if entry_type == "User" else "cursor-entry"
            link_class = "toc-link toc-user" if entry_type == "User" else "toc-link toc-cursor"

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
    def build_tree(items: list[tuple[int, str, str]], start_idx: int = 0, current_level: int = 2, indent: int = 8) -> tuple[str, int]:
        """Recursively build nested list structure."""
        html_parts = []
        i = start_idx
        indent_str = " " * indent

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

                html_parts.append(f"{indent_str}</li>")
            else:
                # This shouldn't happen if structure is correct, but handle it
                break

        tree_html = "\n".join(html_parts)
        if tree_html.strip():
            return f"{indent_str}<ul>\n{tree_html}\n{indent_str}</ul>", i
        return "", i

    tree_html, _ = build_tree(filtered_headings)

    if not tree_html:
        return ""

    # Remove the outer <ul> wrapper since we already have .toc-list
    tree_html = tree_html.strip()
    if tree_html.startswith("<ul>") and tree_html.endswith("</ul>"):
        # Extract content between <ul> tags
        tree_html = tree_html[4:-5].strip()

    toc_html = f"""    <div class="table-of-contents">
        <h2 id="table-of-contents">Table of Contents</h2>
        <ul class="toc-list">
{tree_html}
        </ul>
    </div>"""

    return toc_html


def add_back_to_top_links(html_content: str) -> str:
    """Add 'Back to TOC' links after h2 headings and User/Cursor entries, excluding the Table of Contents heading."""
    # Pattern to match h2 headings, but exclude the table-of-contents one
    h2_pattern = re.compile(r'(<h2 id="table-of-contents">.*?</h2>)|(<h2[^>]*>.*?</h2>)', re.DOTALL)

    def add_back_link_h2(match: re.Match[str]) -> str:
        h2_tag = match.group(0)
        # Skip if this is the table-of-contents heading
        if 'id="table-of-contents"' in h2_tag:
            return h2_tag
        return f'{h2_tag}\n    <div class="back-to-top"><a href="#table-of-contents">↑ Back to TOC</a></div>'

    html_content = h2_pattern.sub(add_back_link_h2, html_content)

    # Pattern to match User/Cursor paragraphs with IDs
    user_cursor_pattern = re.compile(
        r'(<p id="(user|cursor)-\d+"><strong>(User|Cursor)</strong></p>)', re.IGNORECASE
    )

    def add_back_link_user_cursor(match: re.Match[str]) -> str:
        p_tag = match.group(0)
        return f'{p_tag}\n    <div class="back-to-top"><a href="#table-of-contents">↑ Back to TOC</a></div>'

    html_content = user_cursor_pattern.sub(add_back_link_user_cursor, html_content)

    return html_content


def generate_html_document(html_body: str, title: str | None = None) -> str:
    """Generate a complete HTML document with Liatrio styling.

    Args:
        html_body: The HTML body content (already processed with IDs, TOC, etc.)
        title: Optional title. If not provided, extracts from first h1 or uses default.

    Returns:
        Complete HTML document as string.
    """
    # Get title from first heading or use provided/default
    if title is None:
        title_match = re.search(r"<h1[^>]*>(.*?)</h1>", html_body, re.DOTALL)
        if title_match:
            title_text = re.sub(r"<[^>]+>", "", title_match.group(1))
            title = f"{title_text} - Liatrio Documentation"
        else:
            title = "Document - Liatrio Documentation"

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

    return html_document

