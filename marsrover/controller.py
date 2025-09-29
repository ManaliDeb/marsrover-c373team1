# orchestration (Mission), DI entrypoints
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
        it = iter(lines)
        plateau = parse_plateau(next(it))
        results: List[str] = []
        cmd_map = command_factory(self.movement_policy, plateau)

        while True:
            try: rover_line = next(it)
            except StopIteration: break
            rover_line = rover_line.strip()
            if rover_line == "": continue
            pos: Position = parse_position(rover_line, plateau)
            commands = parse_commands(next(it))
            for c in commands:
                pos = cmd_map[c].apply(pos)
            results.append(f"{pos.x} {pos.y} {pos.heading.value}")
        return results
