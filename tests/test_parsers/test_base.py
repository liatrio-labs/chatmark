"""Unit tests for parser base class interface."""

import pytest

from chatmark.parsers.base import BaseParser


class TestBaseParser:
    """Tests for BaseParser abstract base class."""

    def test_parse_method_exists(self):
        """Test that BaseParser has parse method."""
        assert hasattr(BaseParser, "parse")

    def test_parse_is_abstract(self):
        """Test that BaseParser cannot be instantiated directly."""
        with pytest.raises(TypeError):
            BaseParser()  # type: ignore

    def test_concrete_parser_must_implement_parse(self):
        """Test that concrete parser must implement parse method."""

        class IncompleteParser(BaseParser):
            pass

        with pytest.raises(TypeError):
            IncompleteParser()  # type: ignore

    def test_parse_returns_string(self):
        """Test that parse method returns a string."""

        class ConcreteParser(BaseParser):
            def parse(self, content: str) -> str:
                return "**User**\n\nTest\n\n**AI**\n\nResponse"

        parser = ConcreteParser()
        result = parser.parse("test input")
        assert isinstance(result, str)

    def test_parse_outputs_internal_format(self):
        """Test that parse outputs internal markdown format standard."""

        class ConcreteParser(BaseParser):
            def parse(self, content: str) -> str:
                return "**User**\n\nTest\n\n**AI**\n\nResponse"

        parser = ConcreteParser()
        result = parser.parse("test")
        # Should contain User/AI markers
        assert "**User**" in result
        assert "**AI**" in result

    def test_parse_handles_empty_input(self):
        """Test that parse handles empty input gracefully."""

        class ConcreteParser(BaseParser):
            def parse(self, content: str) -> str:
                return "" if not content else "**User**\n\n" + content

        parser = ConcreteParser()
        result = parser.parse("")
        assert isinstance(result, str)

    def test_parse_handles_invalid_input(self):
        """Test that parse handles invalid input gracefully."""

        class ConcreteParser(BaseParser):
            def parse(self, content: str) -> str:
                # Should not raise exception, return empty or error format
                if not content or len(content) < 3:
                    return ""
                return "**User**\n\n" + content

        parser = ConcreteParser()
        # Should not raise exception
        result = parser.parse("x")
        assert isinstance(result, str)
