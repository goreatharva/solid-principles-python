from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

"""
S — Single Responsibility Principle (SRP)

A class should have only one reason to change.
- `Report` builds the report content (business rule).
- `ReportSaver` persists the content (I/O concern).
"""

@dataclass
class Report:
    title: str
    lines: list[str]

    def render_text(self) -> str:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        body = '\n'.join(self.lines)
        return f"# {self.title}\nGenerated: {timestamp}\n\n{body}\n"

class ReportSaver:
    def save_to_file(self, content: str, path: str) -> None:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

    def save_lines(self, lines: Iterable[str], path: str) -> None:
        with open(path, 'w', encoding='utf-8') as f:
            for line in lines:
                f.write(f"{line}\n")