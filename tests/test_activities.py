"""
Tests for the get_activities endpoint.
"""
import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities."""
    response = client.get("/activities")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    
    # Check that expected activities are present
    expected_activities = [
        "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
        "Science Olympiad", "Art Studio", "Soccer Club", "Debate Team",
        "Music Band", "Tennis Club", "Robotics Club", "Drama Club"
    ]
    for activity in expected_activities:
        assert activity in data


def test_get_activities_has_required_fields(client):
    """Test that each activity has required fields."""
    response = client.get("/activities")
    data = response.json()
    
    required_fields = ["description", "schedule", "max_participants", "participants"]
    
    for activity_name, activity_data in data.items():
        for field in required_fields:
            assert field in activity_data, f"Activity '{activity_name}' missing field '{field}'"


def test_get_activities_participants_is_list(client):
    """Test that participants field is a list for each activity."""
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity_data in data.items():
        assert isinstance(activity_data["participants"], list), \
            f"Activity '{activity_name}' participants field is not a list"


def test_get_activities_initial_participants(client):
    """Test that initial participants are correctly set."""
    response = client.get("/activities")
    data = response.json()
    
    # Chess Club should have 2 participants
    assert len(data["Chess Club"]["participants"]) == 2
    assert "michael@mergington.edu" in data["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in data["Chess Club"]["participants"]
    
    # Basketball Team should have 0 participants
    assert len(data["Basketball Team"]["participants"]) == 0
