# 01-tasks-package-refactor-vscode-support.md

## Relevant Files

- `chatmark/__init__.py` - Package initialization file with version export.
- `chatmark/core/__init__.py` - Core module initialization.
- `chatmark/core/converter.py` - Core conversion orchestration logic extracted from `md_to_html.py`.
- `chatmark/core/html_generator.py` - HTML generation logic including ToC generation, ID addition, and HTML document assembly.
- `chatmark/core/styles.py` - Liatrio CSS styling extracted from `md_to_html.py`.
- `chatmark/parsers/__init__.py` - Parsers module initialization.
- `chatmark/parsers/base.py` - Abstract base class for parsers defining the parser interface.
- `chatmark/parsers/cursor_md.py` - Cursor markdown parser that normalizes Cursor exports to internal markdown format standard.
- `chatmark/parsers/vscode.py` - VS Code JSON parser that extracts conversation flow and converts to internal markdown format standard.
- `chatmark/exporters/__init__.py` - Exporters module initialization.
- `chatmark/exporters/base.py` - Abstract base class for exporters defining the exporter interface.
- `chatmark/exporters/markdown.py` - Markdown exporter that outputs the exact internal markdown format standard for round-trip compatibility (no transformations, passes through internal format as-is).
- `chatmark/exporters/html.py` - HTML exporter that uses `core.html_generator` to produce HTML output.
- `chatmark/exporters/pdf.py` - PDF exporter that uses WeasyPrint to generate PDF files from HTML.
- `chatmark/cli.py` - Typer CLI application with `convert` command supporting format and export options.
- `tests/conftest.py` - Pytest configuration file with shared fixtures for test data and setup.
- `tests/test_core/__init__.py` - Core tests module initialization.
- `tests/test_core/test_converter.py` - Unit tests for core conversion orchestration logic.
- `tests/test_core/test_html_generator.py` - Unit tests for HTML generation functions (ToC, IDs, document assembly).
- `tests/test_parsers/__init__.py` - Parser tests module initialization.
- `tests/test_parsers/test_base.py` - Unit tests for parser base class interface.
- `tests/test_parsers/test_cursor_md.py` - Unit tests for Cursor markdown parser.
- `tests/test_parsers/test_vscode_parser.py` - Unit tests for VS Code JSON parser.
- `tests/test_exporters/__init__.py` - Exporter tests module initialization.
- `tests/test_exporters/test_base.py` - Unit tests for exporter base class interface.
- `tests/test_exporters/test_markdown.py` - Unit tests for markdown exporter.
- `tests/test_exporters/test_html.py` - Unit tests for HTML exporter.
- `tests/test_exporters/test_pdf.py` - Unit tests for PDF exporter.
- `tests/integration/__init__.py` - Integration tests module initialization.
- `tests/integration/test_cli_cursor.py` - Integration tests for CLI with Cursor markdown input.
- `tests/integration/test_cli_vscode.py` - Integration tests for CLI with VS Code JSON input.
- `tests/integration/test_cli_exports.py` - Integration tests for all export formats (markdown, HTML, PDF).
- `tests/fixtures/cursor_sample.md` - Sample Cursor markdown file for testing (based on `examples/cursor-ide-example.md`).
- `tests/fixtures/vscode_sample.json` - Sample VS Code JSON file for testing (based on `examples/vs-code-ide-example.json`).
- `pyproject.toml` - Update to add CLI entry point `[project.scripts]` section and ensure pytest-cov is in dev dependencies.
- `README.md` - Update documentation to reflect new package structure and CLI usage.

### Notes

- Unit tests should be placed alongside the code files they are testing (e.g., `test_core/` for `core/` module tests).
- Use the repository's established testing command: `uv run pytest tests/` with configuration from `pyproject.toml`.
- Follow the repository's existing code organization, naming conventions, and style guidelines (ruff configuration: line-length 100, double quotes, py311 target).
- Adhere to identified quality gates: ruff linting/formatting, pre-commit hooks, and CI pipeline checks.
- Follow strict TDD workflow: write tests first (red phase), implement to pass tests (green phase), refactor while maintaining passing tests.
- All parsers must convert their input to the tool's internal markdown format standard (`**User**` and `**AI**` markers).
- All exporters consume the internal markdown format standard as input.

## Internal Markdown Format Specification

The tool uses a canonical internal markdown format standard that serves as the intermediate representation between parsers and exporters. This ensures consistent output regardless of input format.

### Format Structure

**Basic Format:**

```markdown
**User**

<user_request_text>

**AI**

<ai_response_text>
```

**Multi-Turn Conversation Example:**

```markdown
**User**

How do I parse JSON in Python?

**AI**

You can use the `json` module in Python's standard library:

[code block with python syntax]

**User**

What about handling errors?

**AI**

You can wrap it in a try-except block:

[code block with python syntax]
```

Note: Code blocks within the internal format use standard markdown fenced code syntax (triple backticks with language identifier).

### Marker Rules

1. **Markers**: Conversation entries are marked with `**User**` or `**AI**` as paragraph-level markers (bold markdown syntax)
2. **Normalization**: All AI responses are standardized to `**AI**` marker regardless of source tool (e.g., `**Cursor**` from Cursor exports is normalized to `**AI**`)
3. **Placement**: Markers must be on their own line, followed by two newlines before the content
4. **Detection**: User/AI entry detection uses regex patterns matching these exact markers

### Content Handling

- **Code Blocks**: Standard markdown fenced code blocks (triple backticks) are preserved
- **Metadata**: Any metadata from source formats (timestamps, file references) should be preserved as markdown comments or inline text
- **Special Characters**: Standard markdown escaping rules apply
- **Nested Formatting**: Standard markdown formatting (bold, italic, links) is preserved within entries

### Edge Cases

- **Empty Entries**: Empty user requests or AI responses should still include the marker followed by empty content
- **Escaped Markers**: If source content contains literal `**User**` or `**AI**` text, it should be escaped or marked differently to avoid confusion
- **Whitespace**: Leading/trailing whitespace in entries should be preserved as-is
- **Multiple Paragraphs**: Multi-paragraph entries are separated by single newlines within the entry

### Round-Trip Compatibility

The markdown exporter outputs this exact format without transformation, ensuring that:

- Parser → Internal Format → Markdown Exporter produces identical output to direct markdown input
- All exporters consume the same internal format, ensuring consistent behavior

## Tasks

- [x] 1.0 Establish TDD Infrastructure and Package Structure
  - Demo Criteria: "Test infrastructure established with `tests/` directory, `conftest.py` with pytest fixtures, and test discovery working. Package structure exists with `chatmark/` containing `core/`, `parsers/`, `exporters/`, and `cli.py`. Unit tests written first (TDD red phase) for core conversion functions, then implementation passes tests (green phase). All existing Cursor markdown-to-HTML functionality works through the new package structure. CLI command `chatmark` is available and functional with integration tests. Test fixtures directory created with sample Cursor markdown files."
  - Proof Artifact(s): "Test infrastructure: `uv run pytest tests/ -v` runs successfully. Directory structure: `tree chatmark/` and `tree tests/` showing organized modules. CLI help output: `chatmark --help` showing available commands. Successful Cursor markdown conversion: `chatmark convert examples/cursor-ide-example.md --format cursor-md --export html --output test.html`. Test output: `uv run pytest tests/ -v` showing passing tests for core functionality. Test fixtures: `tests/fixtures/` directory with Cursor markdown samples."
  - [x] 1.1 Create test infrastructure: Create `tests/` directory structure with `conftest.py` containing pytest fixtures for test data and file paths. Ensure test discovery works with `uv run pytest tests/ -v`.
  - [x] 1.1a Add pytest-cov dependency: Add `pytest-cov` to `[dependency-groups.dev]` in `pyproject.toml`. Verify configuration is recognized by running `uv sync` and confirming `pytest-cov` is available. This ensures test coverage reporting works in milestone 1.
  - [x] 1.2 Create test fixtures: Create `tests/fixtures/` directory and add `cursor_sample.md` fixture file based on `examples/cursor-ide-example.md` (use a smaller representative sample).
  - [x] 1.3 Create package structure: Create `chatmark/` package directory with `__init__.py` (exporting version), and subdirectories `core/`, `parsers/`, `exporters/` each with `__init__.py` files.
  - [x] 1.4 Extract CSS styles: Create `chatmark/core/styles.py` and extract `LIATRIO_CSS` constant from `md_to_html.py` (lines 52-540). The CSS constant contains Liatrio dark theme styling including CSS variables for brand colors, typography, code blocks, tables, and table of contents styling. Extract the entire multi-line string constant as-is, preserving all formatting. Add proper module docstring explaining this is the Liatrio brand CSS for HTML output styling.
  - [x] 1.5 Write tests for HTML generator utilities (TDD red): Create `tests/test_core/test_html_generator.py` with unit tests for `slugify`, `add_heading_ids`, `add_user_cursor_ids`, `extract_user_cursor_entries_from_html`, `extract_headings`, `generate_table_of_contents`, and `add_back_to_top_links` functions. Tests should initially fail.
  - [x] 1.6 Implement HTML generator utilities (TDD green): Create `chatmark/core/html_generator.py` and implement all utility functions from `md_to_html.py` to pass tests. Include proper type hints and docstrings.
  - [x] 1.7 Write tests for HTML document generation (TDD red): Add tests to `tests/test_core/test_html_generator.py` for complete HTML document generation including title extraction, CSS injection, and document structure.
  - [x] 1.8 Implement HTML document generation (TDD green): Add HTML document assembly logic to `html_generator.py` to pass tests.
  - [x] 1.9 Write tests for converter orchestration (TDD red): Create `tests/test_core/test_converter.py` with tests for conversion workflow: reading markdown, parsing, HTML generation, and file output.
  - [x] 1.10 Implement converter orchestration (TDD green): Create `chatmark/core/converter.py` with conversion orchestration logic extracted from `md_to_html.py`'s `convert_markdown_to_html` function.
  - [x] 1.10a Write tests for parser base interface (TDD red): Create `tests/test_parsers/test_base.py` with tests validating the abstract parser contract. Test that `parse()` method exists, returns a string, handles invalid input gracefully, and enforces the internal markdown format standard output. Tests should initially fail since base class doesn't exist yet.
  - [x] 1.11 Create parser base class: Create `chatmark/parsers/base.py` with abstract base class defining `parse()` method that returns internal markdown format standard string. Implement to pass tests from 1.10a.
  - [x] 1.12 Write tests for Cursor markdown parser (TDD red): Create `tests/test_parsers/test_cursor_md.py` with tests for parsing Cursor markdown and normalizing `**Cursor**` markers to `**AI**` in internal format.
  - [x] 1.13 Implement Cursor markdown parser (TDD green): Create `chatmark/parsers/cursor_md.py` implementing parser base class to pass tests.
  - [x] 1.13a Write tests for exporter base interface (TDD red): Create `tests/test_exporters/test_base.py` with tests validating the abstract exporter contract. Test that `export()` method exists, accepts a string (internal markdown format standard), handles edge cases (empty input, invalid format), and enforces the expected interface. Tests should initially fail since base class doesn't exist yet.
  - [x] 1.14 Create exporter base class: Create `chatmark/exporters/base.py` with abstract base class defining `export()` method that accepts internal markdown format standard string. Implement to pass tests from 1.13a.
  - [x] 1.15 Write tests for HTML exporter (TDD red): Create `tests/test_exporters/test_html.py` with tests for HTML exporter that consumes internal markdown format and produces HTML output.
  - [x] 1.16 Implement HTML exporter (TDD green): Create `chatmark/exporters/html.py` implementing exporter base class using `core.html_generator` to pass tests.
  - [x] 1.17 Write tests for CLI (TDD red): Create `tests/integration/test_cli_cursor.py` with integration tests for CLI `convert` command with Cursor markdown input and HTML export.
  - [x] 1.18 Implement CLI (TDD green): Create `chatmark/cli.py` with Typer app and `convert` command supporting `--format cursor-md` and `--export html` options. Register CLI entry point in `pyproject.toml` under `[project.scripts]`.
  - [x] 1.19 Verify end-to-end functionality: Run integration tests and manual CLI tests to ensure Cursor markdown-to-HTML conversion works through new package structure. All tests should pass.

- [x] 2.0 Implement VS Code JSON Parser with TDD
  - Demo Criteria: "Unit tests written first for VS Code parser (TDD red phase). VS Code JSON parser extracts basic conversation flow (requests/responses with text) and passes tests (green phase). Parser converts VS Code JSON to the tool's internal markdown format standard. CLI accepts `--format vscode` flag and successfully processes VS Code JSON files. Parser handles basic edge cases (empty responses, missing fields) with tests. Integration tests verify CLI functionality with VS Code JSON input."
  - Proof Artifact(s): "Test output: `uv run pytest tests/test_parsers/test_vscode_parser.py -v` showing passing parser tests. Successful VS Code conversion: `chatmark convert examples/vs-code-ide-example.json --format vscode --export markdown --output test.md`. Generated markdown file showing User/AI conversation entries conforming to the tool's internal markdown format standard. Test fixtures: `tests/fixtures/vscode_*.json` with sample VS Code exports. Integration test output: `uv run pytest tests/integration/test_cli_vscode.py -v` showing CLI integration tests passing."
  - [x] 2.1 Create VS Code test fixture: Create `tests/fixtures/vscode_sample.json` based on `examples/vs-code-ide-example.json` (use a smaller representative sample with multiple requests/responses).
  - [x] 2.2 Write tests for VS Code parser (TDD red): Create `tests/test_parsers/test_vscode_parser.py` with unit tests for parsing VS Code JSON structure: extracting text from `requests[].message.text` and `requests[].message.parts[].text` for requests, extracting text from `requests[].response[].value` for responses, and converting to internal markdown format standard (`**User**` and `**AI**` markers).
  - [x] 2.3 Write tests for VS Code edge cases (TDD red): Add tests to `test_vscode_parser.py` for edge cases: empty responses array, missing `message.text` field, missing `response` array, malformed JSON structure, and code reference handling (displaying file references like `example.file:21-22` with markup).
  - [x] 2.4 Implement VS Code parser (TDD green): Create `chatmark/parsers/vscode.py` implementing parser base class to extract conversation flow and convert to internal markdown format standard. Handle edge cases and code references as specified in tests.
  - [x] 2.5 Write tests for markdown exporter (TDD red): Create `tests/test_exporters/test_markdown.py` with tests for markdown exporter that outputs internal markdown format standard (ensuring round-trip compatibility). Test that the exporter passes through the internal format exactly without transformation, preserving all markers, formatting, and content structure. Verify round-trip: parse → internal format → markdown export produces identical output to original input.
  - [x] 2.6 Implement markdown exporter (TDD green): Create `chatmark/exporters/markdown.py` implementing exporter base class to pass tests. Output should match internal format standard exactly (no transformations, passes through internal format as-is). Add module docstring clarifying this exporter's purpose: round-trip compatibility by outputting the exact internal markdown format standard without modification.
  - [x] 2.7 Update CLI to support VS Code format: Update `chatmark/cli.py` to accept `--format vscode` option and route to VS Code parser.
  - [x] 2.8 Write integration tests for VS Code CLI (TDD red): Create `tests/integration/test_cli_vscode.py` with integration tests for CLI `convert` command with VS Code JSON input and markdown export.
  - [x] 2.9 Verify VS Code end-to-end functionality: Run integration tests and manual CLI tests to ensure VS Code JSON-to-markdown conversion works. All tests should pass.

- [ ] 3.0 Implement Multi-Format Export Support with TDD
  - Demo Criteria: "Unit tests written first for each exporter (TDD red phase). CLI supports `--export markdown`, `--export html`, and `--export pdf` options. VS Code JSON can be exported to all three formats with passing tests (green phase). Cursor markdown input can be exported to all three formats. PDF generation works correctly with proper styling and tests. Integration tests verify end-to-end CLI functionality for all export formats."
  - Proof Artifact(s): "CLI help showing export options: `chatmark convert --help`. Successful exports from Cursor markdown: Three output files (`.md`, `.html`, `.pdf`) generated from `examples/cursor-ide-example.md` using `--format cursor-md`. Successful exports from VS Code JSON: Three output files (`.md`, `.html`, `.pdf`) generated from `examples/vs-code-ide-example.json`. Test output: `uv run pytest tests/test_exporters/ -v` showing passing exporter tests for both input formats. Generated PDF files open correctly and display formatted content. Integration test output: `uv run pytest tests/integration/test_cli_exports.py -v` showing all export format tests passing. Test coverage: `uv run pytest tests/ --cov=chatmark --cov-report=term-missing` showing >80% coverage for core modules."
  - [ ] 3.1 Write tests for PDF exporter (TDD red): Create `tests/test_exporters/test_pdf.py` with unit tests for PDF exporter that consumes internal markdown format, converts to HTML, and generates PDF using WeasyPrint with proper styling.
  - [ ] 3.2 Implement PDF exporter (TDD green): Create `chatmark/exporters/pdf.py` implementing exporter base class using WeasyPrint to generate PDF files. Extract PDF-specific CSS from `md_to_html.py`'s `convert_html_to_pdf` function (lines 912-1063). The PDF CSS includes page setup, dark theme color preservation, page break handling, and code wrapping rules. Extract the entire `pdf_css` string constant and organize appropriately (consider adding to `core/styles.py` as `PDF_CSS` or keeping in exporter module).
  - [ ] 3.3 Update CLI to support all export formats: Update `chatmark/cli.py` to accept `--export` option with values `markdown`, `html`, and `pdf`. Route to appropriate exporter based on selection.
  - [ ] 3.4 Write integration tests for all export formats (TDD red): Create `tests/integration/test_cli_exports.py` with integration tests for all export format combinations: Cursor markdown → markdown/html/pdf, VS Code JSON → markdown/html/pdf.
  - [ ] 3.5 Verify all export formats end-to-end: Run integration tests and manual CLI tests to ensure all export format combinations work correctly. Generated PDF files should open and display formatted content properly.
  - [ ] 3.6 Verify test coverage: Run `uv run pytest tests/ --cov=chatmark --cov-report=term-missing` and ensure >80% coverage for core modules (`core/`, `parsers/`, `exporters/`). Add additional tests if needed to meet coverage threshold.
  - [ ] 3.7 Update documentation: Update `README.md` to reflect new package structure, CLI usage with `--format` and `--export` options, and testing instructions.
