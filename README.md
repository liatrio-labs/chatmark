# Chatmark

A standalone Typer CLI tool for converting AI conversation exports from
various IDEs and CLI tools (Windsurf, Cursor, VS Code, Claude Code, Codex CLI,
Cursor Agent CLI, etc.) to beautifully styled HTML and PDF versions for easy
sharing.

## Purpose

This tool transforms AI conversation exports (`.md` and `.json`) from various AI tools into
professional, shareable HTML and PDF documents with:

- **Liatrio Dark Theme Styling**: Beautiful dark theme using Liatrio brand colors
- **Automatic Table of Contents**: Smart ToC generation with support for
  User/AI conversation entries
- **Navigation Features**: Anchor links and "Back to TOC" navigation
- **PDF Export**: Optional PDF generation with optimized page breaks and code wrapping
- **Responsive Design**: Works well on desktop and mobile devices

## Current State

The tool is now a proper Python package with a modern CLI (`chatmark`) that:

- Converts AI conversation exports from multiple formats (Cursor markdown, VS Code JSON) to various output formats (Markdown, HTML, PDF)
- Generates table of contents automatically
- Supports User/AI conversation entry detection
- Uses internal markdown format standard for consistent output
- Generates PDF versions using WeasyPrint with optimized styling
- Uses `uv` for dependency management with `pyproject.toml`
- Includes comprehensive test suite with TDD workflow
- Includes CI/CD pipeline for automated testing and linting
- Configured with pre-commit hooks for code quality

## Usage

```bash
# Convert Cursor markdown to HTML (default)
chatmark document.md --format cursor-md --export html

# Convert VS Code JSON to markdown
chatmark conversation.json --format vscode --export markdown --output output.md

# Convert to PDF
chatmark document.md --format cursor-md --export pdf --output output.pdf

# All export formats: markdown, html, pdf
# All input formats: cursor-md, vscode
```

### CLI Options

- `--format` / `-f`: Input format (`cursor-md`, `vscode`) - default: `cursor-md`
- `--export` / `-e`: Export format (`markdown`, `html`, `pdf`) - default: `html`
- `--output` / `-o`: Output file path (optional, defaults to input filename with appropriate extension)

## Next Steps for Conversion

To make this a fully standalone, production-ready tool, the following
improvements are needed:

### 1. Project Structure

- [x] Create proper `pyproject.toml` with project metadata
- [x] Set up package structure (`chatmark/` with `core/`, `parsers/`, `exporters/`)
- [x] Add proper dependency management
- [x] Create installation instructions

### 2. Enhanced Input Format Support

- [x] Support direct export formats from various IDEs (VS Code JSON)
- [x] Add format specification via CLI (`--format` flag)
- [ ] Support batch processing of multiple files
- [ ] Add directory processing mode

### 3. Configuration & Customization

- [ ] Add config file support for theme customization
- [ ] Support custom CSS themes
- [ ] Add command-line options for styling tweaks
- [ ] Support custom templates

### 4. Testing & Quality

- [x] Add unit tests for conversion functions
- [x] Add integration tests for CLI
- [x] Add test fixtures with sample conversations
- [x] Set up CI/CD pipeline
- [x] Achieve >80% test coverage for core modules

### 5. Documentation

- [ ] Expand usage examples
- [ ] Add API documentation
- [ ] Create user guide for different IDE exports
- [ ] Add troubleshooting section

### 6. Features

- [ ] Add support for code syntax highlighting
- [ ] Add export options (single file, multiple formats)
- [ ] Add metadata extraction (dates, participants, etc.)
- [ ] Add search functionality in generated HTML
- [ ] Support for attachments/media in conversations

### 7. Distribution

- [ ] Package for PyPI
- [ ] Create installation script
- [ ] Add pre-built binaries (if applicable)
- [ ] Create Docker image option

## Development

### Requirements

- Python 3.11+
- `uv` (for dependency management and script execution)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd chatmark

# Install dependencies with uv
uv sync

# Run the CLI tool
uv run chatmark document.md --format cursor-md --export html
```

### Dependencies

Dependencies are managed via `pyproject.toml` and can be installed with `uv sync`:

**Runtime dependencies:**

- `markdown>=3.5` - Markdown parsing
- `typer>=0.12` - CLI framework
- `rich>=13.0` - Terminal output formatting
- `weasyprint>=62.0` - PDF generation

**Development dependencies:**

- `ruff>=0.14.4` - Linting and formatting
- `pytest>=9.0.1` - Testing framework
- `pytest-cov>=6.0.0` - Test coverage reporting
- `pre-commit>=4.4.0` - Git hooks

### Testing

Run the test suite:

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=chatmark --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_parsers/test_vscode_parser.py -v
```

## License

[To be determined]
