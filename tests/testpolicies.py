from marsrover.controller import Mission
from marsrover.policies import ToroidalMovement

def test_wraps_around_edges_with_toroidal_policy():
    lines = ["1 1\n", "1 1 N\n", "M\n"]  # would go to (1,2) on 1x1 board -> wraps to (1,0)
    out = Mission(ToroidalMovement()).run_io_lines(lines)
    assert out == ["1 0 N"]
