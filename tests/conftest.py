"""Pytest configuration file with shared fixtures for test data and setup."""

from pathlib import Path

import pytest


@pytest.fixture
def fixtures_dir() -> Path:
    """Return the path to the test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def examples_dir() -> Path:
    """Return the path to the examples directory."""
    return Path(__file__).parent.parent / "examples"


@pytest.fixture
def cursor_sample_md(fixtures_dir: Path) -> Path:
    """Return the path to the Cursor markdown sample fixture."""
    return fixtures_dir / "cursor_sample.md"


@pytest.fixture
def vscode_sample_json(fixtures_dir: Path) -> Path:
    """Return the path to the VS Code JSON sample fixture."""
    return fixtures_dir / "vscode_sample.json"


@pytest.fixture
def cursor_example_md(examples_dir: Path) -> Path:
    """Return the path to the Cursor markdown example file."""
    return examples_dir / "cursor-ide-example.md"


@pytest.fixture
def vscode_example_json(examples_dir: Path) -> Path:
    """Return the path to the VS Code JSON example file."""
    return examples_dir / "vs-code-ide-example.json"


@pytest.fixture
def temp_output_dir(tmp_path: Path) -> Path:
    """Return a temporary directory for test output files."""
    return tmp_path / "output"
