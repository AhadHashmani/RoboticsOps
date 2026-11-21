"""
Streamlit dashboard for a simulated warehouse fleet.

The robot rows, tasks, and metrics below are local literals. This file does
not call the FastAPI app or the Claude agent.
"""

import subprocess
import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def get_robots():
    return [
        {"id": "AGV-001", "status": "active", "battery": 85, "task": "Pick SKU-001"},
        {"id": "AGV-002", "status": "active", "battery": 92, "task": "Transport to Station-3"},
        {"id": "AGV-003", "status": "idle", "battery": 78, "task": "None"},
        {"id": "AGV-004", "status": "charging", "battery": 45, "task": "None"},
    ]


def get_metrics():
    return {
        "total_robots": 4,
        "active_robots": 2,
        "pending_tasks": 12,
        "completed_today": 156,
        "efficiency": 94.2
    }


def main():
    """Render the dashboard. Streamlit reruns this on each interaction."""
    st.set_page_config(
        page_title="RoboticsOps Dashboard",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

    st.title("🤖 RoboticsOps Dashboard")
    st.markdown("Simulated warehouse fleet. These figures are sample data, not live robots.")

    st.sidebar.title("⚙️ Controls")
    view = st.sidebar.radio(
        "Select View",
        ["Overview", "Robots", "Tasks", "Analytics", "AI Agent"]
    )

    if view == "Overview":
        col1, col2, col3, col4, col5 = st.columns(5)

        metrics = get_metrics()

        with col1:
            st.metric("🤖 Total Robots", metrics["total_robots"])
        with col2:
            st.metric("✅ Active", metrics["active_robots"])
        with col3:
            st.metric("📦 Pending Tasks", metrics["pending_tasks"])
        with col4:
            st.metric("✓ Completed", metrics["completed_today"])
        with col5:
            st.metric("📊 Efficiency", f"{metrics['efficiency']}%")

        st.divider()

        st.subheader("Warehouse Layout")
        fig = go.Figure()

        robots = get_robots()
        for i, robot in enumerate(robots):
            status_color = {"active": "green", "idle": "gray", "charging": "orange"}[robot["status"]]
            fig.add_trace(go.Scatter(
                x=[45 + (i * 10)], y=[25 + (i * 5)],
                mode="markers+text",
                marker=dict(size=20, color=status_color),
                text=[robot["id"]],
                textposition="top center"
            ))

        fig.update_layout(
            title="Sample robot positions",
            xaxis_title="X Position (m)",
            yaxis_title="Y Position (m)",
            hovermode="closest",
            height=500,
            xaxis=dict(range=[0, 100]),
            yaxis=dict(range=[0, 50])
        )

        st.plotly_chart(fig, use_container_width=True)

    elif view == "Robots":
        st.subheader("Robot Status")
        robots = get_robots()
        df = pd.DataFrame(robots)
        st.dataframe(df, use_container_width=True)

        selected_robot = st.selectbox("Select Robot", [r["id"] for r in robots])
        st.write(f"Selected: {selected_robot}")

    elif view == "Tasks":
        st.subheader("Active Tasks")
        tasks = [
            {"task_id": "T-001", "robot": "AGV-001", "type": "Pick", "location": "Station-1", "progress": 60},
            {"task_id": "T-002", "robot": "AGV-002", "type": "Transport", "location": "Station-3", "progress": 45},
            {"task_id": "T-003", "robot": "None", "type": "Sort", "location": "Station-5", "progress": 0},
        ]

        for task in tasks:
            with st.container():
                col1, col2, col3 = st.columns([2, 1, 2])
                with col1:
                    st.write(f"**{task['task_id']}** - {task['type']} @ {task['location']}")
                with col2:
                    st.write(f"Robot: {task['robot']}")
                with col3:
                    st.progress(task['progress']/100, text=f"{task['progress']}%")

    elif view == "Analytics":
        st.subheader("Performance Metrics")
        st.caption("Random sample drawn on each rerun. Not a measurement.")

        import numpy as np
        dates = pd.date_range("2025-05-01", periods=30)
        efficiency = np.random.randint(85, 99, 30)
        tasks_completed = np.random.randint(40, 60, 30)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=efficiency, name="Efficiency %", yaxis="y"))
        fig.add_trace(go.Bar(x=dates, y=tasks_completed, name="Tasks Completed", yaxis="y2"))

        fig.update_layout(
            title="Sample 30-day series",
            yaxis=dict(title="Efficiency %"),
            yaxis2=dict(title="Tasks Completed", overlaying="y", side="right"),
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

    elif view == "AI Agent":
        st.subheader("🤖 AI Orchestration Agent")
        st.info("This view does not call Claude. Agent mode is a separate process.")

        st.write("Type a command:")
        command = st.text_input("Command", placeholder="e.g., 'Optimize robot allocation'")

        if st.button("Execute"):
            st.success(f"No agent is connected. Command not sent: {command}")


def run_dashboard():
    """Launch `streamlit run` for this file. Importing the module does not start the UI."""
    script = str(Path(__file__).resolve())
    cmd = [
        sys.executable, "-m", "streamlit", "run", script,
        "--server.headless", "true",
        "--server.port", "8501",
        "--browser.gatherUsageStats", "false",
    ]
    raise SystemExit(subprocess.call(cmd))


if __name__ == "__main__":
    main()
