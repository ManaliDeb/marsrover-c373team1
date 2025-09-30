#todo

import pytest
from marsrover.io import parse_mission, run_mission_text

EXAMPLE = """\
5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM
"""

def _dim(plateau):
    # support either (width,height) or (max_x,max_y)
    w = getattr(plateau, "width", getattr(plateau, "max_x"))
    h = getattr(plateau, "height", getattr(plateau, "max_y"))
    return w, h

def test_parse_mission_two_rovers_and_commands():
    plateau, pairs = parse_mission(EXAMPLE.splitlines())
    w, h = _dim(plateau)
    assert (w, h) == (5, 5)
    assert len(pairs) == 2
    # commands-only assertions to avoid coupling to rover internals
    _, cmds1 = pairs[0]
    _, cmds2 = pairs[1]
    assert cmds1 == "LMLMLMLMM"
    assert cmds2 == "MMRMMRMRRM"

def test_run_mission_text_matches_kata_example():
    out = run_mission_text(EXAMPLE)
    assert out.strip().splitlines() == ["1 3 N", "5 1 E"]

def test_empty_input_raises():
    with pytest.raises(ValueError):
        parse_mission([])

def test_dangling_rover_without_commands_raises():
    bad = """\
5 5
1 2 N
"""
    with pytest.raises(ValueError):
        parse_mission(bad.splitlines())

def test_landing_out_of_bounds_raises():
    bad = """\
5 5
7 0 N
MMMM
"""
    with pytest.raises(ValueError):
        parse_mission(bad.splitlines())