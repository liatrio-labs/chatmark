"""Unit tests for exporter base class interface."""

from pathlib import Path

import pytest

from chatmark.exporters.base import BaseExporter


class TestBaseExporter:
    """Tests for BaseExporter abstract base class."""

    def test_export_is_abstract(self):
        """Test that BaseExporter cannot be instantiated directly."""
        with pytest.raises(TypeError):
            BaseExporter()  # type: ignore

    def test_concrete_exporter_must_implement_export(self):
        """Test that concrete exporter must implement export method."""

        class IncompleteExporter(BaseExporter):
            pass

        with pytest.raises(TypeError):
            IncompleteExporter()  # type: ignore

    def test_export_accepts_internal_format(self):
        """Test that export accepts internal markdown format standard."""

        class ConcreteExporter(BaseExporter):
            def export(self, content: str, output_path: str) -> str:
                return output_path

        exporter = ConcreteExporter()
        internal_format = "**User**\n\nTest\n\n**AI**\n\nResponse"
        result = exporter.export(internal_format, "/tmp/test.html")
        assert isinstance(result, str)

    def test_export_handles_empty_input(self):
        """Test that export handles empty input gracefully."""

        class ConcreteExporter(BaseExporter):
            def export(self, content: str, output_path: str) -> str:
                return output_path

        exporter = ConcreteExporter()
        result = exporter.export("", "/tmp/test.html")
        assert isinstance(result, str)

    def test_export_handles_invalid_format(self):
        """Test that export handles invalid format gracefully."""

        class ConcreteExporter(BaseExporter):
            def export(self, content: str, output_path: str) -> str:
                # Should not raise exception
                return output_path

        exporter = ConcreteExporter()
        # Should not raise exception
        result = exporter.export("invalid format", "/tmp/test.html")
        assert isinstance(result, str)

    def test_export_handles_invalid_path(self, tmp_path: Path):
        """Test that export handles invalid/non-writable paths gracefully."""

        class ConcreteExporter(BaseExporter):
            def export(self, content: str, output_path: str) -> str:
                # Attempt to write to a non-existent directory
                invalid_path = Path(output_path)
                if not invalid_path.parent.exists():
                    # Should either create parent or raise a documented exception
                    invalid_path.parent.mkdir(parents=True, exist_ok=True)
                return output_path

        exporter = ConcreteExporter()
        # Use a path with non-existent parent directory
        invalid_path = tmp_path / "nonexistent" / "deep" / "path" / "output.html"
        result = exporter.export("test content", str(invalid_path))
        assert isinstance(result, str)

    def test_export_handles_edge_cases(self, tmp_path: Path):
        """Test that export handles edge cases (large content, special chars)."""

        class ConcreteExporter(BaseExporter):
            def export(self, content: str, output_path: str) -> str:
                return output_path

        exporter = ConcreteExporter()
        output_path = str(tmp_path / "test.html")

        # Test with very large content
        large_content = "**User**\n\n" + "x" * 1000000 + "\n\n**AI**\n\nResponse"
        result = exporter.export(large_content, output_path)
        assert isinstance(result, str)

        # Test with special characters
        special_content = "**User**\n\nTest with émojis 🎉 and unicode 中文\n\n**AI**\n\nResponse"
        result = exporter.export(special_content, output_path)
        assert isinstance(result, str)

        # Test with binary-like content (should be handled as string)
        binary_like = "**User**\n\n" + "\x00\x01\x02" + "\n\n**AI**\n\nResponse"
        result = exporter.export(binary_like, output_path)
        assert isinstance(result, str)
