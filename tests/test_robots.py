"""
Robot configuration tests.
"""

import pytest
from backend.api import Robot


def test_robot_creation():
    """Test robot model creation."""
    robot = Robot(
        id="AGV-001",
        status="active",
        battery=85.0,
        position=(45.2, 23.5),
        current_task="Pick SKU-001"
    )
    assert robot.id == "AGV-001"
    assert robot.status == "active"
    assert robot.battery == 85.0


def test_robot_validation():
    """Test robot validation."""
    with pytest.raises(Exception):
        # This will fail due to invalid battery value
        Robot(
            id="AGV-001",
            status="invalid_status",
            battery="not_a_number",
            position=(45.2, 23.5)
        )
