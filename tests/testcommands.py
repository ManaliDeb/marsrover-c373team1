"""Tests for command pattern implementation."""
import pytest
from marsrover.commands import TurnLeft, TurnRight, command_factory
from marsrover.domain import Position, Heading, Plateau
from marsrover.policies import BoundedMovement, ToroidalMovement
from marsrover.parsing import parse_commands


class TestTurnLeft:
    def test_turn_left_from_north(self):
        cmd = TurnLeft()
        pos = Position(1, 1, Heading.N)
        result = cmd.apply(pos)
        assert result.heading == Heading.W
        assert result.x == 1 and result.y == 1

    def test_turn_left_from_west(self):
        cmd = TurnLeft()
        pos = Position(2, 3, Heading.W)
        result = cmd.apply(pos)
        assert result.heading == Heading.S

    def test_turn_left_from_south(self):
        cmd = TurnLeft()
        pos = Position(0, 0, Heading.S)
        result = cmd.apply(pos)
        assert result.heading == Heading.E

    def test_turn_left_from_east(self):
        cmd = TurnLeft()
        pos = Position(5, 5, Heading.E)
        result = cmd.apply(pos)
        assert result.heading == Heading.N

    def test_turn_left_preserves_position(self):
        cmd = TurnLeft()
        pos = Position(3, 4, Heading.N)
        result = cmd.apply(pos)
        assert (result.x, result.y) == (3, 4)


class TestTurnRight:
    def test_turn_right_from_north(self):
        cmd = TurnRight()
        pos = Position(1, 1, Heading.N)
        result = cmd.apply(pos)
        assert result.heading == Heading.E
        assert result.x == 1 and result.y == 1

    def test_turn_right_from_east(self):
        cmd = TurnRight()
        pos = Position(2, 3, Heading.E)
        result = cmd.apply(pos)
        assert result.heading == Heading.S

    def test_turn_right_from_south(self):
        cmd = TurnRight()
        pos = Position(0, 0, Heading.S)
        result = cmd.apply(pos)
        assert result.heading == Heading.W

    def test_turn_right_from_west(self):
        cmd = TurnRight()
        pos = Position(5, 5, Heading.W)
        result = cmd.apply(pos)
        assert result.heading == Heading.N

    def test_turn_right_preserves_position(self):
        cmd = TurnRight()
        pos = Position(3, 4, Heading.N)
        result = cmd.apply(pos)
        assert (result.x, result.y) == (3, 4)


class TestCommandFactory:
    def test_factory_creates_left_command(self):
        plateau = Plateau(5, 5)
        policy = BoundedMovement()
        cmd_map = command_factory(policy, plateau)
        assert "L" in cmd_map
        pos = Position(2, 2, Heading.N)
        result = cmd_map["L"].apply(pos)
        assert result.heading == Heading.W

    def test_factory_creates_right_command(self):
        plateau = Plateau(5, 5)
        policy = BoundedMovement()
        cmd_map = command_factory(policy, plateau)
        assert "R" in cmd_map
        pos = Position(2, 2, Heading.N)
        result = cmd_map["R"].apply(pos)
        assert result.heading == Heading.E

    def test_factory_creates_move_command(self):
        plateau = Plateau(5, 5)
        policy = BoundedMovement()
        cmd_map = command_factory(policy, plateau)
        assert "M" in cmd_map
        pos = Position(2, 2, Heading.N)
        result = cmd_map["M"].apply(pos)
        assert result.y == 3  # moved north

    def test_factory_binds_plateau_to_move(self):
        plateau = Plateau(3, 3)
        policy = BoundedMovement()
        cmd_map = command_factory(policy, plateau)
        pos = Position(3, 3, Heading.N)
        with pytest.raises(ValueError, match="Move would leave plateau"):
            cmd_map["M"].apply(pos)

    def test_factory_with_toroidal_policy(self):
        plateau = Plateau(2, 2)
        policy = ToroidalMovement()
        cmd_map = command_factory(policy, plateau)
        pos = Position(2, 2, Heading.N)
        result = cmd_map["M"].apply(pos)
        assert result.y == 0  # wrapped

    def test_factory_all_commands_present(self):
        plateau = Plateau(5, 5)
        policy = BoundedMovement()
        cmd_map = command_factory(policy, plateau)
        assert set(cmd_map.keys()) == {"L", "R", "M"}

    def test_factory_commands_are_reusable(self):
        plateau = Plateau(5, 5)
        policy = BoundedMovement()
        cmd_map = command_factory(policy, plateau)
        pos1 = Position(1, 1, Heading.N)
        pos2 = cmd_map["L"].apply(pos1)
        pos3 = cmd_map["L"].apply(pos2)
        assert pos3.heading == Heading.S


class TestInvalidCommands:
    def test_parse_commands_rejects_unknown(self):
        with pytest.raises(ValueError):
            parse_commands("MX")  # mirrors the old unknown-command test
