from marsrover.controller import Mission

def test_sample_io():
    lines = [
        "5 5\n",
        "1 2 N\n", "LMLMLMLMM\n",
        "3 3 E\n", "MMRMMRMRRM\n",
    ]
    assert Mission().run_io_lines(lines) == ["1 3 N", "5 1 E"]
