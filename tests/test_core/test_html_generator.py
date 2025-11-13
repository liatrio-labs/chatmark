"""Unit tests for HTML generator utilities."""

from chatmark.core.html_generator import (
    add_back_to_top_links,
    add_heading_ids,
    add_user_cursor_ids,
    extract_headings,
    extract_user_cursor_entries_from_html,
    generate_html_document,
    generate_table_of_contents,
    slugify,
)


class TestSlugify:
    """Tests for slugify function."""

    def test_simple_text(self):
        """Test slugify with simple text."""
        assert slugify("Hello World") == "hello-world"

    def test_text_with_special_chars(self):
        """Test slugify removes special characters."""
        assert slugify("Hello, World!") == "hello-world"

    def test_text_with_multiple_spaces(self):
        """Test slugify collapses multiple spaces."""
        assert slugify("Hello    World") == "hello-world"

    def test_text_with_leading_trailing_hyphens(self):
        """Test slugify strips leading/trailing hyphens."""
        assert slugify("-Hello World-") == "hello-world"

    def test_empty_string(self):
        """Test slugify with empty string."""
        assert slugify("") == ""

    def test_unicode_characters(self):
        """Test slugify handles unicode characters (preserves them)."""
        # The regex \w includes unicode word characters, so they are preserved
        assert slugify("Café Müñoz") == "café-müñoz"


class TestAddHeadingIds:
    """Tests for add_heading_ids function."""

    def test_single_heading(self):
        """Test adding ID to a single heading."""
        html = "<h1>Hello World</h1>"
        result = add_heading_ids(html)
        assert 'id="hello-world"' in result
        assert "<h1 id=" in result

    def test_multiple_headings(self):
        """Test adding IDs to multiple headings."""
        html = "<h1>First</h1><h2>Second</h2>"
        result = add_heading_ids(html)
        assert 'id="first"' in result
        assert 'id="second"' in result

    def test_heading_with_html_content(self):
        """Test heading with HTML content inside."""
        html = "<h2>Hello <strong>World</strong></h2>"
        result = add_heading_ids(html)
        assert 'id="hello-world"' in result
        assert "<strong>World</strong>" in result

    def test_all_heading_levels(self):
        """Test all heading levels h1-h6."""
        html = "<h1>One</h1><h2>Two</h2><h3>Three</h3><h4>Four</h4><h5>Five</h5><h6>Six</h6>"
        result = add_heading_ids(html)
        for level in range(1, 7):
            assert f"<h{level} id=" in result


class TestAddUserCursorIds:
    """Tests for add_user_cursor_ids function."""

    def test_single_user_entry(self):
        """Test adding ID to a single User entry."""
        html = "<p><strong>User</strong></p>"
        result = add_user_cursor_ids(html)
        assert 'id="user-1"' in result

    def test_single_cursor_entry(self):
        """Test adding ID to a single Cursor entry."""
        html = "<p><strong>Cursor</strong></p>"
        result = add_user_cursor_ids(html)
        assert 'id="cursor-1"' in result

    def test_multiple_user_entries(self):
        """Test adding sequential IDs to multiple User entries."""
        html = "<p><strong>User</strong></p><p><strong>User</strong></p>"
        result = add_user_cursor_ids(html)
        assert 'id="user-1"' in result
        assert 'id="user-2"' in result

    def test_mixed_user_cursor_entries(self):
        """Test adding IDs to mixed User and Cursor entries."""
        html = (
            "<p><strong>User</strong></p><p><strong>Cursor</strong></p><p><strong>User</strong></p>"
        )
        result = add_user_cursor_ids(html)
        assert 'id="user-1"' in result
        assert 'id="cursor-1"' in result
        assert 'id="user-2"' in result

    def test_case_insensitive(self):
        """Test that matching is case insensitive."""
        html = "<p><strong>USER</strong></p><p><strong>cursor</strong></p>"
        result = add_user_cursor_ids(html)
        assert 'id="user-1"' in result
        assert 'id="cursor-1"' in result


class TestExtractUserCursorEntriesFromHtml:
    """Tests for extract_user_cursor_entries_from_html function."""

    def test_single_user_entry(self):
        """Test extracting a single User entry."""
        html = '<p id="user-1"><strong>User</strong></p><p>Some content</p>'
        entries = extract_user_cursor_entries_from_html(html)
        assert len(entries) == 1
        assert entries[0]["type"] == "User"
        assert entries[0]["id"] == "user-1"
        assert entries[0]["number"] == 1

    def test_single_cursor_entry(self):
        """Test extracting a single Cursor entry."""
        html = '<p id="cursor-1"><strong>Cursor</strong></p><p>Some content</p>'
        entries = extract_user_cursor_entries_from_html(html)
        assert len(entries) == 1
        assert entries[0]["type"] == "Cursor"
        assert entries[0]["id"] == "cursor-1"
        assert entries[0]["number"] == 1

    def test_multiple_entries(self):
        """Test extracting multiple entries."""
        html = (
            '<p id="user-1"><strong>User</strong></p><p>First</p>'
            '<p id="cursor-1"><strong>Cursor</strong></p><p>Second</p>'
        )
        entries = extract_user_cursor_entries_from_html(html)
        assert len(entries) == 2
        assert entries[0]["type"] == "User"
        assert entries[1]["type"] == "Cursor"

    def test_preview_text_extraction(self):
        """Test that preview text is extracted from next paragraph."""
        html = '<p id="user-1"><strong>User</strong></p><p>This is the preview text content</p>'
        entries = extract_user_cursor_entries_from_html(html)
        assert entries[0]["preview"] == "This is the preview text content"

    def test_preview_text_truncation(self):
        """Test that preview text is truncated to 100 characters."""
        long_text = "a" * 150
        html = f'<p id="user-1"><strong>User</strong></p><p>{long_text}</p>'
        entries = extract_user_cursor_entries_from_html(html)
        assert len(entries[0]["preview"]) == 100
        assert entries[0]["preview"].endswith("...")

    def test_no_entries(self):
        """Test with no User/Cursor entries."""
        html = "<p>Just regular content</p>"
        entries = extract_user_cursor_entries_from_html(html)
        assert len(entries) == 0


class TestExtractHeadings:
    """Tests for extract_headings function."""

    def test_single_heading(self):
        """Test extracting a single heading."""
        html = '<h1 id="hello-world">Hello World</h1>'
        headings = extract_headings(html)
        assert len(headings) == 1
        assert headings[0] == (1, "hello-world", "Hello World")

    def test_multiple_headings(self):
        """Test extracting multiple headings."""
        html = '<h1 id="first">First</h1><h2 id="second">Second</h2>'
        headings = extract_headings(html)
        assert len(headings) == 2
        assert headings[0] == (1, "first", "First")
        assert headings[1] == (2, "second", "Second")

    def test_heading_with_html_content(self):
        """Test extracting heading with HTML content."""
        html = '<h2 id="test">Hello <strong>World</strong></h2>'
        headings = extract_headings(html)
        assert headings[0][2] == "Hello World"

    def test_no_headings(self):
        """Test with no headings."""
        html = "<p>Just content</p>"
        headings = extract_headings(html)
        assert len(headings) == 0


class TestGenerateTableOfContents:
    """Tests for generate_table_of_contents function."""

    def test_empty_headings(self):
        """Test with empty headings list."""
        assert generate_table_of_contents([]) == ""

    def test_headings_only(self):
        """Test generating TOC from headings."""
        headings = [(2, "section-1", "Section 1"), (3, "subsection-1", "Subsection 1")]
        toc = generate_table_of_contents(headings)
        assert "table-of-contents" in toc
        assert "Section 1" in toc
        assert 'href="#section-1"' in toc

    def test_user_cursor_entries(self):
        """Test generating TOC from User/Cursor entries."""
        entries = [
            {"type": "User", "id": "user-1", "number": 1, "preview": "First question"},
            {"type": "Cursor", "id": "cursor-1", "number": 1, "preview": "First answer"},
        ]
        toc = generate_table_of_contents([], user_cursor_entries=entries)
        assert "table-of-contents" in toc
        assert "User 1" in toc
        assert "Cursor 1" in toc
        assert 'href="#user-1"' in toc
        assert 'href="#cursor-1"' in toc

    def test_user_cursor_entries_override_headings(self):
        """Test that User/Cursor entries take precedence over headings."""
        headings = [(2, "section-1", "Section 1")]
        entries = [{"type": "User", "id": "user-1", "number": 1, "preview": "Question"}]
        toc = generate_table_of_contents(headings, user_cursor_entries=entries)
        assert "User 1" in toc
        assert "Section 1" not in toc

    def test_nested_headings(self):
        """Test generating TOC with nested heading structure."""
        headings = [
            (2, "section-1", "Section 1"),
            (3, "subsection-1", "Subsection 1"),
            (3, "subsection-2", "Subsection 2"),
            (2, "section-2", "Section 2"),
        ]
        toc = generate_table_of_contents(headings)
        assert "Section 1" in toc
        assert "Section 2" in toc
        assert "Subsection 1" in toc

    def test_skips_first_h1(self):
        """Test that first h1 is skipped (document title)."""
        headings = [
            (1, "title", "Document Title"),
            (2, "section-1", "Section 1"),
        ]
        toc = generate_table_of_contents(headings)
        assert "Document Title" not in toc
        assert "Section 1" in toc


class TestAddBackToTopLinks:
    """Tests for add_back_to_top_links function."""

    def test_adds_link_after_h2(self):
        """Test adding back-to-top link after h2 heading."""
        html = '<h2 id="section-1">Section 1</h2>'
        result = add_back_to_top_links(html)
        assert "back-to-top" in result
        assert 'href="#table-of-contents"' in result

    def test_skips_table_of_contents_heading(self):
        """Test that TOC heading is skipped."""
        html = '<h2 id="table-of-contents">Table of Contents</h2>'
        result = add_back_to_top_links(html)
        # Should not add link after TOC heading
        assert result.count("back-to-top") == 0

    def test_adds_link_after_user_entry(self):
        """Test adding back-to-top link after User entry."""
        html = '<p id="user-1"><strong>User</strong></p>'
        result = add_back_to_top_links(html)
        assert "back-to-top" in result
        assert 'href="#table-of-contents"' in result

    def test_adds_link_after_cursor_entry(self):
        """Test adding back-to-top link after Cursor entry."""
        html = '<p id="cursor-1"><strong>Cursor</strong></p>'
        result = add_back_to_top_links(html)
        assert "back-to-top" in result
        assert 'href="#table-of-contents"' in result

    def test_multiple_entries(self):
        """Test adding links to multiple entries."""
        html = (
            '<h2 id="section-1">Section 1</h2>'
            '<p id="user-1"><strong>User</strong></p>'
            '<p id="cursor-1"><strong>Cursor</strong></p>'
        )
        result = add_back_to_top_links(html)
        assert result.count("back-to-top") == 3


class TestGenerateHtmlDocument:
    """Tests for generate_html_document function."""

    def test_basic_document_structure(self):
        """Test that document has proper HTML structure."""
        html_body = "<h1>Test Document</h1><p>Content</p>"
        result = generate_html_document(html_body)
        assert "<!DOCTYPE html>" in result
        assert '<html lang="en">' in result
        assert "<head>" in result
        assert "<body>" in result
        assert '<div class="container">' in result

    def test_title_extraction_from_h1(self):
        """Test that title is extracted from first h1 heading."""
        html_body = "<h1>My Document Title</h1><p>Content</p>"
        result = generate_html_document(html_body)
        assert "<title>My Document Title - Liatrio Documentation</title>" in result

    def test_title_fallback_to_default(self):
        """Test that title falls back to default when no h1."""
        html_body = "<p>Content without heading</p>"
        result = generate_html_document(html_body)
        assert "<title>" in result
        assert "Liatrio Documentation" in result

    def test_css_injection(self):
        """Test that CSS is injected into document."""
        html_body = "<h1>Test</h1>"
        result = generate_html_document(html_body)
        assert "<style>" in result
        assert "LIATRIO_CSS" in result or ":root" in result

    def test_font_links(self):
        """Test that Google Fonts links are included."""
        html_body = "<h1>Test</h1>"
        result = generate_html_document(html_body)
        assert "fonts.googleapis.com" in result
        assert "DM+Sans" in result

    def test_meta_tags(self):
        """Test that meta tags are included."""
        html_body = "<h1>Test</h1>"
        result = generate_html_document(html_body)
        assert '<meta charset="UTF-8">' in result
        assert 'name="viewport"' in result

    def test_body_content_preserved(self):
        """Test that body content is preserved in document."""
        html_body = "<h1>Test</h1><p>Some content</p>"
        result = generate_html_document(html_body)
        assert "<h1>Test</h1>" in result
        assert "<p>Some content</p>" in result

    def test_title_with_html_in_h1(self):
        """Test title extraction when h1 contains HTML."""
        html_body = "<h1>Hello <strong>World</strong></h1>"
        result = generate_html_document(html_body)
        # Title should extract text content only
        assert "<title>Hello World - Liatrio Documentation</title>" in result
