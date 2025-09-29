"""Tests for command pattern implementation."""
import pytest
from marsrover.commands import TurnLeft, TurnRight, Move, command_factory
from marsrover.domain import Position, Heading, Plateau
from marsrover.policies import BoundedMovement, ToroidalMovement


class TestTurnLeft:
    """Test the TurnLeft command."""
    
    def test_turn_left_from_north(self):
        cmd = TurnLeft()
        pos = Position(1, 1, Heading.N)
        result = cmd.apply(pos)
        assert result.heading == Heading.W
        assert result.x == 1
        assert result.y == 1
    
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
        assert result.x == 3
        assert result.y == 4


class TestTurnRight:
    """Test the TurnRight command."""
    
    def test_turn_right_from_north(self):
        cmd = TurnRight()
        pos = Position(1, 1, Heading.N)
        result = cmd.apply(pos)
        assert result.heading == Heading.E
        assert result.x == 1
        assert result.y == 1
    
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
        assert result.x == 3
        assert result.y == 4


class TestCommandFactory:
    """Test the command factory function."""
    
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
        assert result.y == 3  # Moved north
    
    def test_factory_binds_plateau_to_move(self):
        """Test that Move command uses the bound plateau."""
        plateau = Plateau(3, 3)
        policy = BoundedMovement()
        cmd_map = command_factory(policy, plateau)
        
        # Try to move off the edge
        pos = Position(3, 3, Heading.N)
        with pytest.raises(ValueError, match="Move would leave plateau"):
            cmd_map["M"].apply(pos)
    
    def test_factory_with_toroidal_policy(self):
        """Test factory with different movement policy."""
        plateau = Plateau(2, 2)
        policy = ToroidalMovement()
        cmd_map = command_factory(policy, plateau)
        
        # Move off edge wraps around
        pos = Position(2, 2, Heading.N)
        result = cmd_map["M"].apply(pos)
        assert result.y == 0  # Wrapped to bottom
    
    def test_factory_all_commands_present(self):
        """Test that factory creates all expected commands."""
        plateau = Plateau(5, 5)
        policy = BoundedMovement()
        cmd_map = command_factory(policy, plateau)
        
        assert set(cmd_map.keys()) == {"L", "R", "M"}
    
    def test_factory_commands_are_reusable(self):
        """Test that commands can be applied multiple times."""
        plateau = Plateau(5, 5)
        policy = BoundedMovement()
        cmd_map = command_factory(policy, plateau)
        
        pos1 = Position(1, 1, Heading.N)
        pos2 = cmd_map["L"].apply(pos1)
        pos3 = cmd_map["L"].apply(pos2)
        
        assert pos3.heading == Heading.S  # Turned left twice


class TestMoveCommand:
    """Test the Move command with different policies."""
    
    def test_move_north_bounded(self):
        plateau = Plateau(5, 5)
        policy = BoundedMovement()
        cmd_map = command_factory(policy, plateau)
        
        pos = Position(2, 2, Heading.N)
        result = cmd_map["M"].apply(pos)
        assert result.x == 2
        assert result.y == 3
        assert result.heading == Heading.N
    
    def test_move_east_bounded(self):
        plateau = Plateau(5, 5)
        policy = BoundedMovement()
        cmd_map = command_factory(policy, plateau)
        
        pos = Position(2, 2, Heading.E)
        result = cmd_map["M"].apply(pos)
        assert result.x == 3
        assert result.y == 2
    
    def test_move_south_bounded(self):
        plateau = Plateau(5, 5)
        policy = BoundedMovement()
        cmd_map = command_factory(policy, plateau)
        
        pos = Position(2, 2, Heading.S)
        result = cmd_map["M"].apply(pos)
        assert result.x == 2
        assert result.y == 1
    
    def test_move_west_bounded(self):
        plateau = Plateau(5, 5)
        policy = BoundedMovement()
        cmd_map = command_factory(policy, plateau)
        
        pos = Position(2, 2, Heading.W)
        result = cmd_map["M"].apply(pos)
        assert result.x == 1
        assert result.y == 2
    
    def test_move_at_boundary_raises_error(self):
        """Test that moving off plateau raises ValueError."""
        plateau = Plateau(5, 5)
        policy = BoundedMovement()
        cmd_map = command_factory(policy, plateau)
        
        # Try to move north from top edge
        pos = Position(3, 5, Heading.N)
        with pytest.raises(ValueError, match="Move would leave plateau"):
            cmd_map["M"].apply(pos)
        
        # Try to move east from right edge
        pos = Position(5, 3, Heading.E)
        with pytest.raises(ValueError, match="Move would leave plateau"):
            cmd_map["M"].apply(pos)
        
        # Try to move south from bottom edge
        pos = Position(3, 0, Heading.S)
        with pytest.raises(ValueError, match="Move would leave plateau"):
            cmd_map["M"].apply(pos)
        
        # Try to move west from left edge
        pos = Position(0, 3, Heading.W)
        with pytest.raises(ValueError, match="Move would leave plateau"):
            cmd_map["M"].apply(pos)