"""
Unit tests for robot orchestration agent.
"""

import pytest
from agent.orchestration import RoboticsAgent


@pytest.fixture
def agent():
    """Create agent instance for testing."""
    return RoboticsAgent()


def test_agent_initialization(agent):
    """Test agent initializes properly."""
    assert agent is not None
    assert len(agent.tools) == 4


def test_tool_definitions(agent):
    """Test tool definitions are valid."""
    tool_names = [tool["name"] for tool in agent.tools]
    assert "query_robot_status" in tool_names
    assert "assign_task_to_robot" in tool_names
    assert "get_warehouse_layout" in tool_names
    assert "predict_completion_time" in tool_names


def test_execute_query_robot_status(agent):
    """Test querying robot status."""
    result = agent._execute_tool("query_robot_status", {"robot_id": "AGV-001"})
    assert result["robot_id"] == "AGV-001"
    assert "status" in result
    assert "battery" in result


def test_execute_assign_task(agent):
    """Test assigning task to robot."""
    result = agent._execute_tool("assign_task_to_robot", {
        "robot_id": "AGV-001",
        "task": "Pick item"
    })
    assert result["success"] == True


def test_execute_get_warehouse_layout(agent):
    """Test getting warehouse layout."""
    result = agent._execute_tool("get_warehouse_layout", {})
    assert "dimensions" in result
    assert "robots" in result
    assert "stations" in result


def test_execute_predict_completion_time(agent):
    """Test predicting completion time."""
    result = agent._execute_tool("predict_completion_time", {
        "robot_id": "AGV-001",
        "task": "Pick item"
    })
    assert "estimated_minutes" in result


def test_execute_invalid_tool(agent):
    """Test executing invalid tool."""
    result = agent._execute_tool("invalid_tool", {})
    assert "error" in result
