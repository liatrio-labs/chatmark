"""Unit tests for VS Code JSON parser."""

import json
import pytest

from chatmark.parsers.vscode import VSCodeParser


class TestVSCodeParser:
    """Tests for VSCodeParser."""

    def test_parser_instantiation(self):
        """Test that parser can be instantiated."""
        parser = VSCodeParser()
        assert parser is not None

    def test_parse_extracts_message_text(self):
        """Test parsing VS Code JSON with message.text field."""
        parser = VSCodeParser()
        json_data = {
            "requests": [
                {
                    "message": {"text": "How do I parse JSON?"},
                    "response": [{"value": "Use the json module."}],
                }
            ]
        }
        content = json.dumps(json_data)
        result = parser.parse(content)

        assert "**User**" in result
        assert "**AI**" in result
        assert "How do I parse JSON?" in result
        assert "Use the json module." in result

    def test_parse_extracts_message_parts_text(self):
        """Test parsing VS Code JSON with message.parts[].text field."""
        parser = VSCodeParser()
        json_data = {
            "requests": [
                {
                    "message": {
                        "parts": [{"text": "What is Python?", "kind": "text"}]
                    },
                    "response": [{"value": "Python is a programming language."}],
                }
            ]
        }
        content = json.dumps(json_data)
        result = parser.parse(content)

        assert "**User**" in result
        assert "**AI**" in result
        assert "What is Python?" in result
        assert "Python is a programming language." in result

    def test_parse_prefers_message_text_over_parts(self):
        """Test that message.text is preferred over message.parts when both exist."""
        parser = VSCodeParser()
        json_data = {
            "requests": [
                {
                    "message": {
                        "text": "Preferred text",
                        "parts": [{"text": "Ignored text", "kind": "text"}],
                    },
                    "response": [{"value": "Response"}],
                }
            ]
        }
        content = json.dumps(json_data)
        result = parser.parse(content)

        assert "Preferred text" in result
        assert "Ignored text" not in result

    def test_parse_handles_multiple_requests(self):
        """Test parsing multiple requests/responses."""
        parser = VSCodeParser()
        json_data = {
            "requests": [
                {
                    "message": {"text": "First question"},
                    "response": [{"value": "First answer"}],
                },
                {
                    "message": {"text": "Second question"},
                    "response": [{"value": "Second answer"}],
                },
            ]
        }
        content = json.dumps(json_data)
        result = parser.parse(content)

        assert result.count("**User**") == 2
        assert result.count("**AI**") == 2
        assert "First question" in result
        assert "First answer" in result
        assert "Second question" in result
        assert "Second answer" in result

    def test_parse_converts_to_internal_format(self):
        """Test that output conforms to internal markdown format standard."""
        parser = VSCodeParser()
        json_data = {
            "requests": [
                {
                    "message": {"text": "Question"},
                    "response": [{"value": "Answer"}],
                }
            ]
        }
        content = json.dumps(json_data)
        result = parser.parse(content)

        # Should have proper format: **User**\n\n<text>\n\n**AI**\n\n<text>
        lines = result.split("\n")
        assert lines[0] == "**User**"
        assert lines[1] == ""  # Empty line after User marker
        assert "Question" in lines[2]
        assert "**AI**" in result
        assert "Answer" in result

    def test_parse_handles_multiple_response_values(self):
        """Test parsing response array with multiple value items."""
        parser = VSCodeParser()
        json_data = {
            "requests": [
                {
                    "message": {"text": "Question"},
                    "response": [
                        {"value": "First part "},
                        {"value": "second part"},
                    ],
                }
            ]
        }
        content = json.dumps(json_data)
        result = parser.parse(content)

        assert "**User**" in result
        assert "**AI**" in result
        assert "First part" in result
        assert "second part" in result

    def test_parse_handles_code_blocks_in_response(self):
        """Test parsing responses with code blocks."""
        parser = VSCodeParser()
        json_data = {
            "requests": [
                {
                    "message": {"text": "Show me code"},
                    "response": [
                        {
                            "value": "Here's some code:\n\n```python\nprint('hello')\n```"
                        }
                    ],
                }
            ]
        }
        content = json.dumps(json_data)
        result = parser.parse(content)

        assert "```python" in result
        assert "print('hello')" in result
        assert "```" in result

    def test_parse_handles_empty_responses_array(self):
        """Test parsing request with empty responses array."""
        parser = VSCodeParser()
        json_data = {
            "requests": [
                {
                    "message": {"text": "Question"},
                    "response": [],
                }
            ]
        }
        content = json.dumps(json_data)
        result = parser.parse(content)

        assert "**User**" in result
        assert "Question" in result
        # Should still have AI marker even if response is empty
        assert "**AI**" in result

    def test_parse_handles_missing_message_text(self):
        """Test parsing request with missing message.text field."""
        parser = VSCodeParser()
        json_data = {
            "requests": [
                {
                    "message": {"parts": [{"text": "From parts", "kind": "text"}]},
                    "response": [{"value": "Response"}],
                }
            ]
        }
        content = json.dumps(json_data)
        result = parser.parse(content)

        assert "**User**" in result
        assert "From parts" in result
        assert "**AI**" in result
        assert "Response" in result

    def test_parse_handles_missing_response_array(self):
        """Test parsing request with missing response array."""
        parser = VSCodeParser()
        json_data = {
            "requests": [
                {
                    "message": {"text": "Question"},
                }
            ]
        }
        content = json.dumps(json_data)
        result = parser.parse(content)

        assert "**User**" in result
        assert "Question" in result
        # Should still have AI marker even if response is missing
        assert "**AI**" in result

    def test_parse_handles_malformed_json(self):
        """Test parsing JSON with invalid structure (missing requests)."""
        parser = VSCodeParser()
        content = '{"invalid": "structure"}'
        
        # Should return empty string when requests key is missing
        result = parser.parse(content)
        assert isinstance(result, str)
        assert result == ""

    def test_parse_handles_empty_requests_array(self):
        """Test parsing JSON with empty requests array."""
        parser = VSCodeParser()
        json_data = {"requests": []}
        content = json.dumps(json_data)
        result = parser.parse(content)

        # Should return empty string or minimal format
        assert isinstance(result, str)

    def test_parse_handles_code_reference_inline(self):
        """Test parsing inlineReference kind in response."""
        parser = VSCodeParser()
        json_data = {
            "requests": [
                {
                    "message": {"text": "Show me example.file:21-22"},
                    "response": [
                        {
                            "kind": "inlineReference",
                            "inlineReference": {
                                "fsPath": "example.file",
                                "location": {
                                    "range": {
                                        "startLineNumber": 21,
                                        "endLineNumber": 22,
                                    }
                                },
                            },
                        },
                        {"value": "Here's the code from that file."},
                    ],
                }
            ]
        }
        content = json.dumps(json_data)
        result = parser.parse(content)

        assert "**User**" in result
        assert "Show me example.file:21-22" in result
        assert "**AI**" in result
        # Should include file reference markup
        assert "example.file" in result or "21-22" in result
        assert "Here's the code from that file." in result

    def test_parse_handles_response_items_without_value(self):
        """Test parsing response items that don't have value field."""
        parser = VSCodeParser()
        json_data = {
            "requests": [
                {
                    "message": {"text": "Question"},
                    "response": [
                        {"kind": "progressTaskSerialized", "content": {"value": "Progress"}},
                        {"value": "Actual response"},
                    ],
                }
            ]
        }
        content = json.dumps(json_data)
        result = parser.parse(content)

        assert "**User**" in result
        assert "**AI**" in result
        # Should extract value from nested content if needed, or skip non-value items
        assert "Actual response" in result

