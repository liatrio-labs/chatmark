"""Typer CLI application for chatmark."""

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from chatmark.exporters.html import HTMLExporter
from chatmark.exporters.markdown import MarkdownExporter
from chatmark.parsers.cursor_md import CursorMarkdownParser
from chatmark.parsers.vscode import VSCodeParser

console = Console()

app = typer.Typer(name="chatmark")


@app.command()
def convert(
    input_file: Annotated[Path, typer.Argument(help="Input file to convert")],
    format: Annotated[
        str, typer.Option("--format", "-f", help="Input format (cursor-md, vscode)")
    ] = "cursor-md",
    export: Annotated[
        str, typer.Option("--export", "-e", help="Export format (markdown, html, pdf)")
    ] = "html",
    output: Annotated[Path | None, typer.Option("--output", "-o", help="Output file path")] = None,
) -> None:
    """Convert AI conversation exports to various formats."""
    if not input_file.exists():
        console.print(f"[bold red]Error:[/] Input file not found: {input_file}")
        raise typer.Exit(1)

    # Parse input based on format
    if format == "cursor-md":
        parser = CursorMarkdownParser()
        content = input_file.read_text(encoding="utf-8")
        internal_format = parser.parse(content)
    elif format == "vscode":
        parser = VSCodeParser()
        content = input_file.read_text(encoding="utf-8")
        try:
            internal_format = parser.parse(content)
        except (ValueError, KeyError) as e:
            console.print(f"[bold red]Error:[/] Failed to parse VS Code JSON: {e}")
            raise typer.Exit(1)
    else:
        console.print(f"[bold red]Error:[/] Unknown format: {format}")
        raise typer.Exit(1)

    # Export based on export format
    if export == "html":
        exporter = HTMLExporter()
        if output is None:
            output = input_file.with_suffix(".html")
        result_path = exporter.export(internal_format, str(output))
        console.print(f"[bold green]Success:[/] Created {result_path}")
    elif export == "markdown":
        exporter = MarkdownExporter()
        if output is None:
            output = input_file.with_suffix(".md")
        result_path = exporter.export(internal_format, str(output))
        console.print(f"[bold green]Success:[/] Created {result_path}")
    elif export == "pdf":
        console.print("[bold red]Error:[/] PDF export not yet implemented")
        raise typer.Exit(1)
    else:
        console.print(f"[bold red]Error:[/] Unknown export format: {export}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
