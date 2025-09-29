# strategy objects (movement policies)
from .domain import Position, Plateau, forward_xy

class BoundedMovement:
    """Reject moves leaving the plateau."""
    def step(self, pos: Position, plateau: Plateau) -> Position:
        dx, dy = forward_xy(pos.heading)
        nx, ny = pos.x + dx, pos.y + dy
        if not plateau.in_bounds(nx, ny):
            raise ValueError(f"Move would leave plateau: ({nx},{ny})")
        return Position(nx, ny, pos.heading)

class ToroidalMovement:
    """Wrap around edges (extra feature)."""
    def step(self, pos: Position, plateau: Plateau) -> Position:
        dx, dy = forward_xy(pos.heading)
        nx = (pos.x + dx) % (plateau.max_x + 1)
        ny = (pos.y + dy) % (plateau.max_y + 1)
        return Position(nx, ny, pos.heading)