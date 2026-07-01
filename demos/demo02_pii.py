"""
===============================================================================
Enterprise AI Gateway (EAIG)

Demo 02

PII Detection & Masking
Which detector found each entity.
For example:
Entity	    Value	            Detector
--------------------------------------------
EMAIL	    ajay@company.com	Presidio
PAN	        ABCDE1234F	        Regex
OPENAI_KEY	sk-...	            Regex

Python 3.13.11
===============================================================================
"""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from security.pii.pii_engine import PIIEngine
from security.pii.pii_types import MaskMode

console = Console()

###############################################################################
SAMPLE_TEXT = """
Employee Record

Name        : Ajay Singala

Email       : ajay.singala@company.com

Phone       : +91 9876543210

PAN         : ABCDE1234F

Aadhaar     : 2345 6789 1234

Passport    : M1234567

Website     : https://company.com

GitHub PAT  :
ghp_abcdefghijklmnopqrstuvwxyz123456789012

OpenAI Key  :
sk-abcdefghijklmnopqrstuvwxyz12345678901234567890
"""

###############################################################################
def print_header():
    console.print()
    console.print(
        Panel.fit(
            "[bold cyan]Enterprise AI Gateway (EAIG)[/bold cyan]\n"
            "Feature 02 : PII Detection & Masking",
            border_style="cyan"
        )
    )


###############################################################################
def print_entities(result):
    table = Table(title="Detected Entities")
    table.add_column("Type", style="cyan")
    table.add_column("Value", style="green")
    table.add_column("Detector")
    table.add_column("Confidence")

    for entity in result.detection_result.entities:
        table.add_row(
            entity.entity_type.value,
            entity.value,
            entity.detector,
            f"{entity.confidence:.2f}"
        )

    console.print(table)

###############################################################################
def print_summary(result):
    table = Table(title="Summary")
    table.add_column("Property")
    table.add_column("Value")

    summary = result.detection_result

    table.add_row(
        "PII Found",
        str(summary.has_pii)
    )

    table.add_row(
        "Entities",
        str(summary.entity_count)
    )

    table.add_row(
        "Risk",
        summary.risk_level.value
    )

    table.add_row(
        "Risk Score",
        str(summary.risk_score)
    )

    console.print(table)

###############################################################################
def run_mode(
    engine,
    mode,
):
    result = engine.process(
        SAMPLE_TEXT,
        mode,
    )

    console.rule(mode.value)
    console.print()
    console.print("[bold]Original[/bold]")
    console.print(SAMPLE_TEXT)
    console.print()
    console.print("[bold]Masked[/bold]")
    console.print(result.masked_text)
    console.print()

    print_entities(result)

    console.print()

    print_summary(result)

    console.print()

###############################################################################
def interactive(engine):
    console.rule("Interactive Mode")

    while True:
        text = console.input(
            "\nEnter text (or exit): "
        )

        if text.lower() == "exit":
            break

        result = engine.process(
            text,
            MaskMode.PLACEHOLDER,
        )

        print_entities(result)

        console.print()
        console.print(result.masked_text)
        console.print()

###############################################################################
def main():
    print_header()

    engine = PIIEngine()

    run_mode(
        engine,
        MaskMode.PLACEHOLDER,
    )

    run_mode(
        engine,
        MaskMode.PARTIAL,
    )

    run_mode(
        engine,
        MaskMode.FULL,
    )

    interactive(engine)

###############################################################################
if __name__ == "__main__":
    main()
