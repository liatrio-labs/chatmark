# 01-spec-package-refactor-vscode-support.md

## Introduction/Overview

This specification defines the refactoring of the `md_to_html.py` script into a proper Python package following modern best practices, and adds support for parsing VS Code IDE conversation exports. The refactoring will transform the single-file script into a well-structured, domain-driven package architecture that supports multiple input formats (Cursor markdown, VS Code JSON) and multiple output formats (Markdown, HTML, PDF). This work establishes a foundation for future extensibility while maintaining clean separation of concerns.

**Internal Markdown Format Standard:** This specification establishes a canonical internal markdown format standard that serves as the intermediate representation for all conversions. This format is the tool's own standard (not tied to any specific IDE format) and defines the structure expected by HTML and PDF exporters. The format uses standardized markers (`**User**` and `**AI**`) regardless of the source tool, ensuring all AI responses are normalized to `**AI**` even if the source format used tool-specific markers (e.g., `**Cursor**`). All input parsers (Cursor markdown, VS Code JSON) convert their input to this internal markdown format, normalizing any tool-specific markers to the standard format, and all exporters (HTML, PDF) consume this format as input.

## Goals

- Refactor `md_to_html.py` into a proper Python package with domain-driven structure
- Implement VS Code JSON parser that converts VS Code conversation exports to the tool's internal markdown format standard
- Create a new CLI entry point (`ai-conversation-converter`) using Typer console scripts
- Establish comprehensive test suite using strict TDD workflow
- Support three output formats: Markdown, HTML, and PDF
- Design architecture for easy addition of future input/output formats

## User Stories

**As a developer**, I want the codebase organized into a proper package structure so that I can easily maintain, test, and extend the functionality.

**As a user**, I want to convert Cursor markdown and VS Code JSON conversation exports to markdown/HTML/PDF so that I can share my AI conversations in a readable format.

**As a user**, I want to explicitly specify input format via CLI flag so that I have control over how my files are processed.

**As a developer**, I want comprehensive test coverage with fixtures so that I can confidently refactor and add features without breaking existing functionality.

**As a user**, I want a consistent CLI interface (`ai-conversation-converter`) so that I can use the tool like other modern Python CLI applications.

## Demoable Units of Work

### [Unit 1]: TDD Infrastructure and Package Structure

**Purpose:** Establish TDD workflow and test infrastructure first, then create the foundation package structure with core conversion logic extracted from the monolithic script.

**Demo Criteria:**

- Test infrastructure established: `tests/` directory structure, `conftest.py` with pytest fixtures, test discovery working
- Package structure exists with `ai_conversation_converter/` directory containing `core/`, `parsers/`, `exporters/`, and `cli.py`
- Unit tests written first (TDD red phase) for core conversion functions, then implementation passes tests (green phase)
- All existing Cursor markdown-to-HTML functionality works through the new package structure with tests
- CLI command `ai-conversation-converter` is available and functional with integration tests
- Test fixtures directory created: `tests/fixtures/` with sample Cursor markdown files

**Proof Artifacts:**

- Test infrastructure: `uv run pytest tests/ -v` runs successfully (may show failing tests initially per TDD)
- Directory structure: `tree ai_conversation_converter/` and `tree tests/` showing organized modules and test structure
- CLI help output: `ai-conversation-converter --help` showing available commands
- Successful Cursor markdown conversion: `ai-conversation-converter convert examples/cursor-ide-example.md --format cursor-md --export html --output test.html`
- Test output: `uv run pytest tests/ -v` showing passing tests for core functionality
- Test fixtures: `tests/fixtures/` directory with Cursor markdown samples (based on `examples/cursor-ide-example.md`)

### [Unit 2]: VS Code JSON Parser with TDD

**Purpose:** Implement VS Code JSON parser following strict TDD: write tests first, then implement parser that extracts conversation content and converts it to the tool's internal markdown format standard.

**Demo Criteria:**

- Unit tests written first for VS Code parser (TDD red phase)
- VS Code JSON parser extracts basic conversation flow (requests/responses with text) and passes tests (green phase)
- Parser converts VS Code JSON to the tool's internal markdown format standard
- CLI accepts `--format vscode` flag and successfully processes VS Code JSON files
- Parser handles basic edge cases (empty responses, missing fields) with tests
- Integration tests verify CLI functionality with VS Code JSON input

**Proof Artifacts:**

- Test output: `uv run pytest tests/test_parsers/test_vscode_parser.py -v` showing passing parser tests
- Successful VS Code conversion: `ai-conversation-converter convert examples/vs-code-ide-example.json --format vscode --export markdown --output test.md`
- Generated markdown file showing User/AI conversation entries conforming to the tool's internal markdown format standard (which matches the structure from `examples/cursor-ide-example.md`)
- Test fixtures: `tests/fixtures/vscode_*.json` with sample VS Code exports (based on `examples/vs-code-ide-example.json`)
- Integration test output: `uv run pytest tests/integration/test_cli_vscode.py -v` showing CLI integration tests passing with `examples/vs-code-ide-example.json`

### [Unit 3]: Multi-Format Export Support with TDD

**Purpose:** Implement multi-format export functionality following TDD: write tests first, then implement exporters for Markdown, HTML, and PDF formats.

**Demo Criteria:**

- Unit tests written first for each exporter (TDD red phase)
- CLI supports `--export markdown`, `--export html`, and `--export pdf` options
- VS Code JSON can be exported to all three formats with passing tests (green phase)
- Cursor markdown input can be exported to all three formats
- PDF generation works correctly with proper styling and tests
- Integration tests verify end-to-end CLI functionality for all export formats

**Proof Artifacts:**

- CLI help showing export options: `ai-conversation-converter convert --help`
- Successful exports from Cursor markdown: Three output files (`.md`, `.html`, `.pdf`) generated from `examples/cursor-ide-example.md` using `--format cursor-md`
- Successful exports from VS Code JSON: Three output files (`.md`, `.html`, `.pdf`) generated from `examples/vs-code-ide-example.json`
- Test output: `uv run pytest tests/test_exporters/ -v` showing passing exporter tests for both input formats
- Generated PDF files open correctly and display formatted content for both example files
- Integration test output: `uv run pytest tests/integration/test_cli_exports.py -v` showing all export format tests passing with both `examples/cursor-ide-example.md` and `examples/vs-code-ide-example.json`
- Test coverage: `uv run pytest tests/ --cov=ai_conversation_converter --cov-report=term-missing` showing >80% coverage for core modules

## Functional Requirements

1. **The system shall** organize code into a domain-driven package structure with `core/`, `parsers/`, and `exporters/` modules.

2. **The system shall** provide a CLI entry point `ai-conversation-converter` registered in `pyproject.toml` using `[project.scripts]`.

3. **The system shall** support parsing VS Code JSON conversation exports and converting them to the tool's internal markdown format standard.

4. **The system shall** extract basic conversation flow from VS Code JSON (request messages and response text content).

5. **The system shall** support explicit format specification via `--format` CLI flag with options: `cursor-md` and `vscode`.

6. **The system shall** support exporting to multiple formats via `--export` CLI flag with options: `markdown`, `html`, and `pdf`.

7. **The system shall** maintain all existing Cursor markdown-to-HTML conversion functionality through the new package structure.

8. **The system shall** generate markdown output from VS Code JSON that conforms to the tool's internal markdown format standard (as defined in lines 206-211), ensuring the output is parseable by existing HTML/PDF exporters' regex patterns that match `**User**` and `**AI**` markers.

9. **The system shall** follow strict TDD workflow: establish test infrastructure first, then write tests before implementing each feature (red phase), implement to pass tests (green phase), and refactor while maintaining passing tests.

10. **The system shall** provide comprehensive unit tests for all parser and exporter modules, written incrementally as each module is developed.

11. **The system shall** provide integration tests that verify CLI functionality end-to-end, written alongside CLI implementation.

12. **The system shall** include test fixtures with realistic sample data for Cursor markdown and VS Code JSON formats, created as part of test infrastructure setup.

13. **The system shall** use pytest fixtures for test setup and teardown following pytest best practices, established in `conftest.py` from the beginning.

14. **The system shall** structure VS Code parser to allow future expansion for metadata extraction (timestamps, agents, code references).

## Non-Goals (Out of Scope)

1. **Auto-detection of input format**: Format detection based on file content or extension is explicitly out of scope for this spec. Users must specify `--format` flag.

2. **Backward compatibility with `md_to_html.py` script**: The old script will be replaced by the new CLI. No migration path or compatibility layer is required.

3. **Full VS Code JSON metadata extraction**: This spec focuses on basic conversation flow only. Advanced metadata (timestamps, agent details, code references) will be structured for future implementation but not implemented now.

4. **Batch processing or directory processing**: Single file processing only. Batch operations are out of scope.

5. **Custom themes or configuration files**: Default Liatrio theme styling only. Theme customization is out of scope.

6. **Additional input formats**: Only Cursor markdown (`cursor-md`) and VS Code JSON (`vscode`) are supported. Cursor JSON format, other IDE formats (Windsurf, Claude Code, etc.), and generic markdown are out of scope.

7. **Code syntax highlighting**: Basic code block rendering only. Syntax highlighting is out of scope.

8. **Search functionality in generated HTML**: Static HTML output only. Interactive features are out of scope.

## Design Considerations

No specific UI/UX design requirements identified. The CLI interface follows standard Typer conventions with clear help text and error messages. Output formats (Markdown, HTML, PDF) maintain existing Liatrio dark theme styling.

## Repository Standards

Implementation must follow established repository patterns and conventions:

- **Minimum Python Version**: Python 3.12

- **Code Style**: Follow `ruff` configuration in `pyproject.toml` (line-length: 100, double quotes, py312 target)

- **Testing**: Use `uv run pytest` with configuration from `pyproject.toml` (test discovery patterns, verbose output)

- **Type Hints**: Use Python 3.12+ type hints throughout (Annotated types for Typer)

- **Documentation**: Include docstrings for all modules, classes, and functions

- **Commit Messages**: Follow conventional commits format (enforced by pre-commit hooks)

- **Pre-commit Hooks**: All code must pass pre-commit checks (ruff, markdownlint, commitlint)

- **CI/CD**: All tests must pass in GitHub Actions CI pipeline

- **Package Structure**: Follow Python packaging best practices with `pyproject.toml` for metadata and dependencies

## Technical Considerations

**Package Structure:**

```text
ai_conversation_converter/
  __init__.py
  core/
    __init__.py
    converter.py          # Core conversion orchestration
    html_generator.py     # HTML generation logic
    styles.py             # CSS styling (extracted from current script)
  parsers/
    __init__.py
    cursor_md.py          # Cursor markdown parser
    vscode.py             # VS Code JSON parser
    base.py               # Abstract base class for parsers
  exporters/
    __init__.py
    markdown.py           # Markdown exporter (outputs internal format standard for round-trip compatibility)
    html.py               # HTML exporter (uses core.html_generator)
    pdf.py                # PDF exporter (uses WeasyPrint)
    base.py               # Abstract base class for exporters
  cli.py                  # Typer CLI application
```

**CLI Entry Point:**

- Register in `pyproject.toml`: `[project.scripts]` with `ai-conversation-converter = "ai_conversation_converter.cli:app"`
- Use Typer's app pattern with subcommands: `convert` command for conversions
- CLI signature: `ai-conversation-converter convert <input_file> --format <format> --export <export_format> [--output <file>]`

**Internal Markdown Format Standard:**

The tool defines its own internal markdown format standard that serves as the canonical intermediate representation:

- Conversation entries are marked with `**User**` or `**AI**` as paragraph-level markers (standardized to `**AI**` for all AI responses regardless of source tool)
- Format: `**User**\n\n<request_text>\n\n**AI**\n\n<response_text>`
- Supports User/AI entry detection via regex patterns matching these markers
- This format is the tool's own standard (not tied to any IDE), though it happens to match Cursor's export format
- All parsers convert their input to this format, normalizing any tool-specific markers (e.g., `**Cursor**` from Cursor exports) to the standard `**AI**` marker
- All exporters consume this format as input

**VS Code JSON Parsing:**

- Parse `requests` array from VS Code JSON structure
- Extract text from `message.text` and `message.parts[].text` for requests
- Extract text from `response[].value` fields for responses
- Convert to the tool's internal markdown format standard: `**User**\n\n<request_text>\n\n**AI**\n\n<response_text>`
- Structure parser class to allow future expansion for metadata fields

**TDD Workflow:**

- Write tests first (red phase)
- Implement minimal code to pass tests (green phase)
- Refactor while keeping tests passing (refactor phase)
- Use pytest fixtures for test data and setup
- Create test fixtures in `tests/fixtures/` directory

**Dependencies:**

- Maintain existing dependencies: `markdown`, `typer`, `rich`, `weasyprint`
- No new runtime dependencies required
- Use `uv run pytest` and `pytest-cov` for testing (pytest-cov already in dev dependencies)

**Error Handling:**

- Validate input file existence and readability
- Validate format flags against supported options
- Provide clear error messages using Rich console
- Handle malformed VS Code JSON gracefully with informative errors

## Success Metrics

1. **Package Structure**: Package successfully installed and importable: `python -c "import ai_conversation_converter; print(ai_conversation_converter.__version__)"`

2. **CLI Functionality**: CLI command available and functional: `ai-conversation-converter --help` shows expected commands

3. **VS Code Parsing**: Successfully parse and convert VS Code JSON: `ai-conversation-converter convert examples/vs-code-ide-example.json --format vscode --export markdown` produces valid markdown conforming to the tool's internal markdown format standard (as defined in lines 206-211), ensuring the output matches the structure expected by existing HTML/PDF exporters' regex patterns and matches the structure from `examples/cursor-ide-example.md`

4. **Test Coverage**: Test coverage >80% for core modules (`core/`, `parsers/`, `exporters/`) achieved incrementally as each module is developed with TDD, tested against both `examples/cursor-ide-example.md` and `examples/vs-code-ide-example.json`

5. **All Tests Passing**: All unit and integration tests pass: `uv run pytest tests/ -v` shows 100% pass rate throughout development (tests written before implementation per TDD), with tests covering both example files

6. **CI Pipeline**: GitHub Actions CI pipeline passes all checks (linting, formatting, tests) with tests running from Unit 1 onwards, validating against both example files

7. **Export Formats**: All three export formats work: Successful generation of `.md`, `.html`, and `.pdf` files from both `examples/cursor-ide-example.md` and `examples/vs-code-ide-example.json`

## Open Questions

1. Should the VS Code parser handle nested conversation structures (followups, multi-turn conversations) or flatten them?
   1. flatten them

2. How should code blocks in VS Code responses be detected and formatted in markdown? (VS Code JSON may have code references vs. actual code blocks)
   1. if a code block is present, render it as normal. if it's just a reference, like `example.file:21-22`, display the file reference along with some markup, something like "Included code from file: `example.file:21-22`".

3. Should the markdown exporter (which outputs the tool's internal markdown format standard) preserve the exact structure needed for HTML/PDF conversion, or can it be a simpler format?
   1. Output the exact internal format, ensuring round-trip compatibility (exported markdown can be re-imported with `--format cursor-md` and converted to HTML/PDF later)

4. What should happen if a VS Code JSON file contains no valid conversation data (empty requests array, malformed structure)?
   1. raise an error that the format is not supported, with instructions to file a bug if the user thinks this is in error

5. Should the CLI support outputting to stdout for markdown export format to enable piping?
   1. no

**Note:** These questions represent design decisions that should be resolved during implementation. They are documented here for reference but do not block specification approval.
