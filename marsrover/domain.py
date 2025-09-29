from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Protocol, Tuple

class Heading(str, Enum):
    N = "N"; E = "E"; S = "S"; W = "W"

LEFT = {Heading.N: Heading.W, Heading.W: Heading.S, Heading.S: Heading.E, Heading.E: Heading.N}
RIGHT = {Heading.N: Heading.E, Heading.E: Heading.S, Heading.S: Heading.W, Heading.W: Heading.N}
DELTA = {Heading.N: (0, 1), Heading.E: (1, 0), Heading.S: (0, -1), Heading.W: (-1, 0)}

@dataclass(frozen=True)
class Plateau:
    max_x: int
    max_y: int
    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x <= self.max_x and 0 <= y <= self.max_y

@dataclass
class Position:
    x: int
    y: int
    heading: Heading

class MovementPolicy(Protocol):
    def step(self, pos: Position, plateau: Plateau) -> Position: ...

def turn_left(h: Heading) -> Heading:  return LEFT[h]
def turn_right(h: Heading) -> Heading: return RIGHT[h]
def forward_xy(h: Heading) -> Tuple[int, int]: return DELTA[h]