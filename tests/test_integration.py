"""
Integration tests for the complete system.
"""

import pytest
from backend.api import create_app


@pytest.fixture
def client():
    """Create FastAPI test client."""
    app = create_app()
    from fastapi.testclient import TestClient
    return TestClient(app)


def test_api_root(client):
    """Test API root endpoint."""
    response = client.get("/")
    assert response.status_code == 200


def test_get_robots(client):
    """Test getting robots."""
    response = client.get("/robots")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_single_robot(client):
    """Test getting single robot."""
    response = client.get("/robots/AGV-001")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "AGV-001"


def test_robot_not_found(client):
    """Test robot not found."""
    response = client.get("/robots/NONEXISTENT")
    assert response.status_code == 404


def test_warehouse_metrics(client):
    """Test warehouse metrics."""
    response = client.get("/warehouse/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "total_robots" in data
    assert "efficiency" in data


def test_health_check(client):
    """Test health check."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
