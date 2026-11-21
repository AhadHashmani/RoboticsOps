"""
RoboticsOps prototype entry point.

RUN_MODE=api starts the FastAPI app.
RUN_MODE=dashboard starts the Streamlit dashboard.
RUN_MODE=agent starts the Claude tool-calling loop and needs ANTHROPIC_API_KEY.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Add paths
sys.path.insert(0, str(Path(__file__).parent))

from agent.orchestration import RoboticsAgent
from backend.api import create_app
from frontend.app import run_dashboard


def main():
    """Main entry point."""
    
    mode = os.getenv("RUN_MODE", "dashboard")  # dashboard, api, or agent
    
    print("=" * 70)
    print("🤖 RoboticsOps: AI-Powered Warehouse Robotics Orchestration")
    print("=" * 70)
    
    if mode == "agent":
        print("Starting AI Agent...")
        agent = RoboticsAgent()
        agent.start()
    
    elif mode == "api":
        print("Starting Backend API...")
        app = create_app()
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
    
    elif mode == "dashboard":
        print("Starting Dashboard...")
        run_dashboard()
    
    else:
        print(f"Unknown mode: {mode}")
        print("Use: dashboard, api, or agent")


if __name__ == "__main__":
    main()
