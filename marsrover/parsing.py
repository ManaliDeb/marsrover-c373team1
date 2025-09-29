from .domain import Plateau, Position, Heading

def parse_plateau(s: str) -> Plateau:
    parts = s.strip().split()
    if len(parts) != 2: raise ValueError("Plateau line must be 'maxX maxY'")
    x, y = map(int, parts)
    if x < 0 or y < 0: raise ValueError("Plateau bounds must be non-negative")
    return Plateau(x, y)

def parse_position(s: str, plateau: Plateau) -> Position:
    parts = s.strip().split()
    if len(parts) != 3: raise ValueError("Rover line must be 'x y H'")
    x, y = map(int, parts[:2]); h = Heading(parts[2].upper())
    if not plateau.in_bounds(x, y): raise ValueError("Initial position out of bounds")
    return Position(x, y, h)

def parse_commands(s: str) -> str:
    seq = s.strip().upper()
    if any(c not in "LRM" for c in seq):
        raise ValueError("Invalid command in sequence")
    return seq
