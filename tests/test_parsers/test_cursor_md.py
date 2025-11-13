"""Unit tests for Cursor markdown parser."""

from chatmark.parsers.cursor_md import CursorMarkdownParser


class TestCursorMarkdownParser:
    """Tests for CursorMarkdownParser."""

    def test_parse_normalizes_cursor_to_ai(self):
        """Test that **Cursor** markers are normalized to **AI**."""
        parser = CursorMarkdownParser()
        input_md = "**User**\n\nQuestion\n\n**Cursor**\n\nAnswer"
        result = parser.parse(input_md)
        assert "**AI**" in result
        assert "**Cursor**" not in result

    def test_parse_preserves_user_markers(self):
        """Test that **User** markers are preserved."""
        parser = CursorMarkdownParser()
        input_md = "**User**\n\nQuestion\n\n**Cursor**\n\nAnswer"
        result = parser.parse(input_md)
        assert "**User**" in result

    def test_parse_preserves_content(self):
        """Test that content between markers is preserved."""
        parser = CursorMarkdownParser()
        input_md = "**User**\n\nWhat is Python?\n\n**Cursor**\n\nPython is a programming language."
        result = parser.parse(input_md)
        assert "What is Python?" in result
        assert "Python is a programming language." in result

    def test_parse_handles_multiple_exchanges(self):
        """Test parsing multiple User/Cursor exchanges."""
        parser = CursorMarkdownParser()
        input_md = (
            "**User**\n\nFirst question\n\n**Cursor**\n\nFirst answer\n\n"
            "**User**\n\nSecond question\n\n**Cursor**\n\nSecond answer"
        )
        result = parser.parse(input_md)
        assert result.count("**User**") == 2
        assert result.count("**AI**") == 2
        assert "First question" in result
        assert "Second answer" in result

    def test_parse_handles_empty_input(self):
        """Test parsing empty input."""
        parser = CursorMarkdownParser()
        result = parser.parse("")
        assert isinstance(result, str)

    def test_parse_handles_markdown_without_markers(self):
        """Test parsing markdown without User/Cursor markers."""
        parser = CursorMarkdownParser()
        input_md = "# Title\n\nSome content"
        result = parser.parse(input_md)
        assert isinstance(result, str)
        # Should return the content as-is or in internal format
        assert len(result) > 0

    def test_parse_case_insensitive_cursor(self):
        """Test that CURSOR (uppercase) is also normalized."""
        parser = CursorMarkdownParser()
        input_md = "**User**\n\nQuestion\n\n**CURSOR**\n\nAnswer"
        result = parser.parse(input_md)
        assert "**AI**" in result
        assert "**CURSOR**" not in result
