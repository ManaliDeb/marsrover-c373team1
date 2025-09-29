#todo

import pytest
from marsrover import Direction, Position, Plateau, Rover, CommandProcessor

def test_command_processor_sequence():
    p = Plateau(5, 5)
    r = Rover(p, Position(1, 2), Direction.N)
    CommandProcessor(r).run("LMLMLMLMM")
    assert (r.position.x, r.position.y, r.heading.value) == (1, 3, "N")

def test_unknown_command_raises():
    p = Plateau(5, 5); r = Rover(p, Position(0, 0), Direction.N)
    with pytest.raises(ValueError):
        CommandProcessor(r).run("MX")