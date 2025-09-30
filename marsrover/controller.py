# orchestration (Mission), DI entrypoints
from __future__ import annotations
from typing import Iterable, List
from .domain import Plateau, Position
from .parsing import parse_plateau, parse_position, parse_commands
from .policies import BoundedMovement
from .commands import command_factory

class Mission:
    """Coordinates plateau, rovers, and commands (DI entrypoint)."""
    def __init__(self, movement_policy=None):
        self.movement_policy = movement_policy or BoundedMovement()

    def run_io_lines(self, lines: Iterable[str]) -> List[str]:
        it = iter(l.strip() for l in lines if l is not None)
        
        # read first non-blank as plateau
        first = next(it, "")
        while first == "":
            first = next(it, None)
            if first is None:
                raise ValueError("Empty mission input")
        plateau: Plateau = parse_plateau(first)

        results: List[str] = []
        cmd_map = command_factory(self.movement_policy, plateau)

        while True:
            try:
                rover_line = next(it)
                while rover_line == "":            # skip blank separators
                    rover_line = next(it)
            except StopIteration:
                break

            pos: Position = parse_position(rover_line, plateau)

            cmd_line = next(it, None)
            
            if cmd_line is None:
                raise ValueError("Dangling rover position without commands")
            commands = parse_commands(cmd_line)
            for c in commands:
                pos = cmd_map[c].apply(pos)
            results.append(f"{pos.x} {pos.y} {pos.heading.value}")
        return results
