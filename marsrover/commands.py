# command pattern for L/R/M
from typing import Protocol, Dict
from .domain import Position, Heading, turn_left, turn_right
from .policies import BoundedMovement

class Command(Protocol):
    def apply(self, pos: Position) -> Position: ...

class TurnLeft:
    def apply(self, pos: Position) -> Position:
        return Position(pos.x, pos.y, turn_left(pos.heading))

class TurnRight:
    def apply(self, pos: Position) -> Position:
        return Position(pos.x, pos.y, turn_right(pos.heading))

class Move:
    def __init__(self, movement_policy=None):
        self.policy = movement_policy or BoundedMovement()
    def apply(self, pos: Position) -> Position:
        # policy consumes plateau via closure later (controller binds it)
        raise RuntimeError("Bind plateau before using")


