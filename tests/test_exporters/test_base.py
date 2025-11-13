"""Unit tests for exporter base class interface."""

import pytest

from chatmark.exporters.base import BaseExporter


class TestBaseExporter:
    """Tests for BaseExporter abstract base class."""

    def test_export_method_exists(self):
        """Test that BaseExporter has export method."""
        assert hasattr(BaseExporter, "export")

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
