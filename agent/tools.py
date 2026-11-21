"""
Tool schemas that RoboticsAgent does not register.

orchestration.py sends its own four tools: query_robot_status,
assign_task_to_robot, get_warehouse_layout, and predict_completion_time.
Nothing in the app imports this module.
"""

from typing import Any, Dict, List, Optional


def define_robotics_tools() -> List[Dict[str, Any]]:
    """Define all available robotics tools."""
    return [
        {
            "name": "query_robot_status",
            "description": "Get real-time status of a warehouse robot",
            "input_schema": {
                "type": "object",
                "properties": {
                    "robot_id": {
                        "type": "string",
                        "description": "Robot ID (AGV-001, AGV-002, etc.)"
                    }
                },
                "required": ["robot_id"]
            }
        },
        {
            "name": "assign_task_to_robot",
            "description": "Assign a warehouse task to a robot",
            "input_schema": {
                "type": "object",
                "properties": {
                    "robot_id": {"type": "string"},
                    "task_type": {
                        "type": "string",
                        "enum": ["pick", "place", "transport", "sort"]
                    },
                    "location": {
                        "type": "string",
                        "description": "Target location (e.g., 'Station-5')"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"]
                    }
                },
                "required": ["robot_id", "task_type", "location"]
            }
        },
        {
            "name": "get_warehouse_metrics",
            "description": "Get current warehouse KPIs",
            "input_schema": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "optimize_task_allocation",
            "description": "Use AI to optimize task allocation across robots",
            "input_schema": {
                "type": "object",
                "properties": {
                    "pending_tasks": {
                        "type": "integer",
                        "description": "Number of pending tasks"
                    }
                }
            }
        }
    ]


def get_tool_by_name(tool_name: str) -> Optional[Dict[str, Any]]:
    """Get a specific tool definition by name."""
    tools = define_robotics_tools()
    for tool in tools:
        if tool["name"] == tool_name:
            return tool
    return None


def validate_tool_input(tool_name: str, tool_input: Dict[str, Any]) -> bool:
    """Validate tool input against schema."""
    tool = get_tool_by_name(tool_name)
    if not tool:
        return False
    
    required = tool["input_schema"].get("required", [])
    for req in required:
        if req not in tool_input:
            return False
    
    return True
