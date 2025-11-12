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

The tool is currently a functional Typer CLI application (`md_to_html.py`) that:

- Converts markdown files to HTML with Liatrio styling
- Generates table of contents automatically
- Supports User/Cursor conversation entry detection
- Optionally generates PDF versions using WeasyPrint
- Uses `uv` for dependency management with `pyproject.toml`
- Includes CI/CD pipeline for automated testing and linting
- Configured with pre-commit hooks for code quality

## Usage

```bash
# Convert with auto-generated timestamp filename
./md_to_html.py document.md

# Convert with custom output filename
./md_to_html.py document.md --output output.html

# Convert and also generate PDF
./md_to_html.py document.md --pdf
```

## Next Steps for Conversion

To make this a fully standalone, production-ready tool, the following
improvements are needed:

### 1. Project Structure

- [x] Create proper `pyproject.toml` with project metadata
- [ ] Set up package structure (if needed)
- [x] Add proper dependency management
- [ ] Create installation instructions

### 2. Enhanced Input Format Support

- [ ] Support direct export formats from various IDEs (JSON, XML, etc.)
- [ ] Add format detection and conversion
- [ ] Support batch processing of multiple files
- [ ] Add directory processing mode

### 3. Configuration & Customization

- [ ] Add config file support for theme customization
- [ ] Support custom CSS themes
- [ ] Add command-line options for styling tweaks
- [ ] Support custom templates

### 4. Testing & Quality

- [ ] Add unit tests for conversion functions
- [ ] Add integration tests for CLI
- [ ] Add test fixtures with sample conversations
- [x] Set up CI/CD pipeline

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

# Run the script (current state - will be replaced by chatmark CLI)
uv run md_to_html.py document.md
```

### Dependencies

Dependencies are managed via `pyproject.toml` and can be installed with `uv sync`:

**Runtime dependencies:**

- `markdown>=3.5`
- `typer>=0.12`
- `rich>=13.0`
- `weasyprint>=62.0` (optional, for PDF generation)

**Development dependencies:**

- `ruff>=0.14.4` (linting and formatting)
- `pytest>=9.0.1` (testing)
- `pre-commit>=4.4.0` (git hooks)

The script also supports PEP 723 inline dependencies for standalone execution.

## License

[To be determined]
