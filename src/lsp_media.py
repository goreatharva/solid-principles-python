
"""L — Liskov Substitution Principle (LSP)

Subtypes must be substitutable for their base types without altering correctness.
Here, `Player` defines `play()` returning a duration. Both `AudioPlayer` and
`VideoPlayer` keep the contract (non-negative duration) and can be used wherever
`Player` is expected.
"""
from __future__ import annotations
from abc import ABC, abstractmethod

class Player(ABC):
    @abstractmethod
    def play(self) -> int:
        ...

class AudioPlayer(Player):
    def __init__(self, duration: int) -> None:
        self.duration = max(0, duration)

    def play(self) -> int:
        return self.duration

class VideoPlayer(Player):
    def __init__(self, duration: int, has_subtitles: bool = False) -> None:
        self.duration = max(0, duration)
        self.has_subtitles = has_subtitles

    def play(self) -> int:
        return self.duration

def total_play_time(players: list[Player]) -> int:
    return sum(p.play() for p in players)
