"""Rich terminal output helpers."""

from __future__ import annotations

from collections import defaultdict

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from uap_signal.models import AnalysisResult, Classification, Release

console = Console()


def print_report(date_label: str, rows: list[tuple[Release, AnalysisResult]]) -> None:
    console.print(f"\n[bold]UAP Signal Report -- {date_label}[/bold]\n")
    grouped: dict[Classification, list[tuple[Release, AnalysisResult]]] = defaultdict(list)
    for row in rows:
        grouped[row[1].classification].append(row)

    for classification in Classification:
        items = grouped.get(classification, [])
        if not items:
            continue
        console.print(f"[bold]{classification.value} ({len(items)} items)[/bold]")
        for release, analysis in items[:10]:
            body = (
                f"[bold]{release.title}[/bold]\n"
                f"Source: {release.source_name} | Credibility: {analysis.source_credibility.value}\n\n"
                f"Summary: {analysis.summary}\n"
                f"Why it matters: {analysis.why_it_matters or '-'}\n"
                f"Novelty: {analysis.novelty_score}/10\n"
                f"URL: {release.url}"
            )
            console.print(Panel(body, expand=False))


def print_sources(rows: list[dict]) -> None:
    table = Table(title="Configured Sources")
    table.add_column("Source")
    table.add_column("Items")
    table.add_column("Last Seen")
    for row in rows:
        table.add_row(str(row["source_name"]), str(row["item_count"]), str(row["last_seen"] or "-"))
    console.print(table)


def print_fetched_table(releases: list[Release]) -> None:
    if not releases:
        console.print("[yellow]No items fetched.[/yellow]")
        return
    table = Table(title=f"Fetched Items ({len(releases)} total)")
    table.add_column("Source")
    table.add_column("Title")
    table.add_column("URL")
    for r in releases:
        title = r.title[:80] + "…" if len(r.title) > 80 else r.title
        table.add_row(r.source_name, title, r.url)
    console.print(table)


def print_cost_estimate(item_count: int) -> None:
    estimated = round(item_count * 0.002, 3)
    console.print(f"[yellow]Dry run:[/yellow] {item_count} items would be analyzed. Estimated LLM cost: ~${estimated}")


def print_source_errors(errors: list[str]) -> None:
    if not errors:
        return
    console.print("[yellow]Source warnings:[/yellow]")
    for error in errors:
        console.print(f"- {error}")
