"""
Claude tool-calling loop for a simulated warehouse fleet.

The handlers in _execute_tool return fixed dictionaries. They do not read
or update the FastAPI robot dict in backend/api.py.
"""

from anthropic import Anthropic
from typing import Dict, List, Any
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RoboticsAgent:
    """Sends warehouse requests to Claude and runs local tool handlers."""
    
    def __init__(self):
        # Created on the first messages call so local tool tests do not need a key.
        self._client = None
        self.model = "claude-3-5-sonnet-20241022"
        self.conversation_history = []
        self.robots = {}  # Robot state
        self.warehouse = {}  # Warehouse state
        self.tools = self._define_tools()

    def _anthropic(self) -> Anthropic:
        if self._client is None:
            self._client = Anthropic()
        return self._client
    
    def _define_tools(self) -> List[Dict[str, Any]]:
        """Define tools for robot control."""
        return [
            {
                "name": "query_robot_status",
                "description": "Check status of a robot (position, battery, task)",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "robot_id": {
                            "type": "string",
                            "description": "Robot identifier (e.g., 'AGV-001')"
                        }
                    },
                    "required": ["robot_id"]
                }
            },
            {
                "name": "assign_task_to_robot",
                "description": "Assign a warehouse task to a specific robot",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "robot_id": {"type": "string"},
                        "task": {"type": "string"},
                        "priority": {
                            "type": "string",
                            "enum": ["low", "medium", "high"]
                        }
                    },
                    "required": ["robot_id", "task"]
                }
            },
            {
                "name": "get_warehouse_layout",
                "description": "Get current warehouse layout and robot positions",
                "input_schema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "predict_completion_time",
                "description": "Predict task completion time based on robot/task",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "robot_id": {"type": "string"},
                        "task": {"type": "string"}
                    },
                    "required": ["robot_id", "task"]
                }
            }
        ]
    
    def start(self):
        """Start interactive agent session."""
        logger.info("Robotics agent started")
        logger.info("Type a request, or exit. The first turn calls Claude and needs ANTHROPIC_API_KEY.")
        
        initial_prompt = """You are an AI-powered warehouse robotics orchestration agent.
        
Your responsibilities:
1. Monitor robot status and health
2. Assign tasks optimally to available robots
3. Predict completion times
4. Optimize warehouse operations
5. Handle conflicts and emergencies

Available robots: AGV-001, AGV-002, AGV-003, AGV-004
Warehouse layout: 100m x 50m with 12 stations

User requests come in. Respond helpfully and use tools when needed."""
        
        self.conversation_history.append({
            "role": "user",
            "content": initial_prompt
        })
        
        # Get initial response
        self._get_agent_response()
        
        # Interactive loop
        while True:
            user_input = input("\n📦 Warehouse Command: ").strip()
            
            if user_input.lower() == "exit":
                logger.info("Shutting down agent...")
                break
            
            if not user_input:
                continue
            
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            self._get_agent_response()
    
    def _get_agent_response(self):
        """Get response from Claude agent."""
        response = self._anthropic().messages.create(
            model=self.model,
            max_tokens=1024,
            tools=self.tools,
            messages=self.conversation_history
        )
        
        # Process response
        assistant_content = []
        for block in response.content:
            if block.type == "text":
                print(f"\n🤖 Agent: {block.text}")
                assistant_content.append(block)
            
            elif block.type == "tool_use":
                logger.info(f"Using tool: {block.name}")
                result = self._execute_tool(block.name, block.input)
                assistant_content.append(block)
                
                self.conversation_history.append({
                    "role": "assistant",
                    "content": assistant_content
                })
                
                self.conversation_history.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(result)
                        }
                    ]
                })
                return
        
        # Add response to history if no tool use
        if response.stop_reason == "end_turn":
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_content
            })
    
    def _execute_tool(self, tool_name: str, tool_input: Dict) -> Dict[str, Any]:
        """Execute a tool."""
        if tool_name == "query_robot_status":
            robot_id = tool_input["robot_id"]
            return {
                "robot_id": robot_id,
                "status": "active",
                "position": [45.2, 23.5],
                "battery": 85,
                "current_task": "Pick item SKU-001",
                "task_progress": 60
            }
        
        elif tool_name == "assign_task_to_robot":
            return {
                "success": True,
                "message": f"Task assigned to {tool_input['robot_id']}",
                "estimated_completion": "2 minutes"
            }
        
        elif tool_name == "get_warehouse_layout":
            return {
                "dimensions": "100m x 50m",
                "robots": [
                    {"id": "AGV-001", "position": [45.2, 23.5]},
                    {"id": "AGV-002", "position": [20.0, 15.0]},
                    {"id": "AGV-003", "position": [75.5, 40.0]},
                    {"id": "AGV-004", "position": [30.0, 35.0]}
                ],
                "stations": 12
            }
        
        elif tool_name == "predict_completion_time":
            return {
                "robot_id": tool_input["robot_id"],
                "task": tool_input["task"],
                "estimated_minutes": 3
            }
        
        return {"error": f"Unknown tool: {tool_name}"}


if __name__ == "__main__":
    agent = RoboticsAgent()
    agent.start()
