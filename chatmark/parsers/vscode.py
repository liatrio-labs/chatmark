"""VS Code JSON parser that extracts conversation flow and converts to internal markdown format."""

import json

from chatmark.parsers.base import BaseParser


class VSCodeParser(BaseParser):
    """Parser for VS Code JSON format that converts to internal markdown format standard.

    This parser extracts conversation flow from VS Code JSON exports and converts them
    to the tool's internal markdown format standard (using **User** and **AI** markers).
    """

    def parse(self, content: str) -> str:
        """Parse VS Code JSON and convert to internal markdown format standard.

        Args:
            content: VS Code JSON content string.

        Returns:
            Markdown string in internal format standard with **User** and **AI** markers.

        Raises:
            ValueError: If JSON is malformed or missing required structure.
            KeyError: If JSON structure is invalid.
        """
        if not content:
            return ""

        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}") from e

        if not isinstance(data, dict):
            raise ValueError("JSON must be an object")

        requests = data.get("requests", [])
        if not isinstance(requests, list):
            raise ValueError("'requests' must be an array")

        if not requests:
            return ""

        result_parts = []

        for request in requests:
            if not isinstance(request, dict):
                continue

            # Extract user message text
            user_text = self._extract_user_text(request)
            if user_text:
                result_parts.append("**User**")
                result_parts.append("")
                result_parts.append(user_text)
                result_parts.append("")

            # Extract AI response text
            ai_text = self._extract_ai_text(request)
            result_parts.append("**AI**")
            result_parts.append("")
            if ai_text:
                result_parts.append(ai_text)
            result_parts.append("")

        return "\n".join(result_parts)

    def _extract_user_text(self, request: dict) -> str:
        """Extract user message text from request.

        Prefers message.text over message.parts[].text.

        Args:
            request: Request dictionary from VS Code JSON.

        Returns:
            User message text, or empty string if not found.
        """
        message = request.get("message", {})
        if not isinstance(message, dict):
            return ""

        # Prefer message.text if it exists
        if "text" in message:
            text = message["text"]
            if isinstance(text, str):
                return text

        # Fall back to message.parts[].text
        parts = message.get("parts", [])
        if isinstance(parts, list):
            text_parts = []
            for part in parts:
                if isinstance(part, dict) and part.get("kind") == "text":
                    text = part.get("text")
                    if isinstance(text, str):
                        text_parts.append(text)
            if text_parts:
                return " ".join(text_parts)

        return ""

    def _extract_ai_text(self, request: dict) -> str:
        """Extract AI response text from request.

        Extracts text from response[].value fields and handles inlineReference
        items for code references.

        Args:
            request: Request dictionary from VS Code JSON.

        Returns:
            AI response text, or empty string if not found.
        """
        response = request.get("response", [])
        if not isinstance(response, list):
            return ""

        if not response:
            return ""

        text_parts = []

        for item in response:
            if not isinstance(item, dict):
                continue

            # Handle inlineReference for code references
            if item.get("kind") == "inlineReference":
                ref = item.get("inlineReference", {})
                if isinstance(ref, dict):
                    fs_path = ref.get("fsPath", "")
                    location = ref.get("location", {})
                    if isinstance(location, dict):
                        range_obj = location.get("range", {})
                        if isinstance(range_obj, dict):
                            start_line = range_obj.get("startLineNumber")
                            end_line = range_obj.get("endLineNumber")
                            if start_line is not None and end_line is not None:
                                ref_text = f"Included code from file: `{fs_path}:{start_line}-{end_line}`"
                                text_parts.append(ref_text)

            # Extract value field (direct or nested in content)
            value = item.get("value")
            if isinstance(value, str):
                text_parts.append(value)
            elif isinstance(value, dict):
                # Handle nested value in content (e.g., progressTaskSerialized)
                nested_value = value.get("value")
                if isinstance(nested_value, str):
                    text_parts.append(nested_value)

            # Handle content.value pattern (for progressTaskSerialized)
            content = item.get("content", {})
            if isinstance(content, dict):
                content_value = content.get("value")
                if isinstance(content_value, str):
                    text_parts.append(content_value)

        return "\n".join(text_parts) if text_parts else ""

