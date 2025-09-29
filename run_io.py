import sys
from marsrover.controller import Mission

if __name__ == "__main__":
    mission = Mission()
    for line in mission.run_io_lines(sys.stdin.readlines()):
        print(line)
