"""
Tests for the unregister endpoint.
"""
import pytest


def test_unregister_success(client):
    """Test successful unregistration from an activity."""
    email = "michael@mergington.edu"
    response = client.post(
        f"/activities/Chess%20Club/unregister?email={email}"
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert "Chess Club" in data["message"]


def test_unregister_removes_participant(client):
    """Test that unregister removes participant from the activity."""
    email = "michael@mergington.edu"
    
    # Get initial participants
    response = client.get("/activities")
    initial_count = len(response.json()["Chess Club"]["participants"])
    assert email in response.json()["Chess Club"]["participants"]
    
    # Unregister
    client.post(f"/activities/Chess%20Club/unregister?email={email}")
    
    # Check that participant was removed
    response = client.get("/activities")
    final_count = len(response.json()["Chess Club"]["participants"])
    assert final_count == initial_count - 1
    assert email not in response.json()["Chess Club"]["participants"]


def test_unregister_nonexistent_activity_fails(client):
    """Test that unregistering from a non-existent activity fails."""
    response = client.post(
        "/activities/Nonexistent%20Activity/unregister?email=test@mergington.edu"
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_nonexistent_participant_fails(client):
    """Test that unregistering a non-participant fails."""
    response = client.post(
        "/activities/Chess%20Club/unregister?email=notregistered@mergington.edu"
    )
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]


def test_unregister_from_empty_activity_fails(client):
    """Test that unregistering from an activity with no participants fails."""
    response = client.post(
        "/activities/Basketball%20Team/unregister?email=test@mergington.edu"
    )
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]


def test_signup_then_unregister(client):
    """Test signing up and then unregistering."""
    email = "testuser@mergington.edu"
    
    # Sign up
    response = client.post(f"/activities/Basketball%20Team/signup?email={email}")
    assert response.status_code == 200
    
    # Verify participant was added
    response = client.get("/activities")
    assert email in response.json()["Basketball Team"]["participants"]
    
    # Unregister
    response = client.post(f"/activities/Basketball%20Team/unregister?email={email}")
    assert response.status_code == 200
    
    # Verify participant was removed
    response = client.get("/activities")
    assert email not in response.json()["Basketball Team"]["participants"]


def test_unregister_multiple_participants(client):
    """Test unregistering one participant doesn't affect others."""
    # Initial state: Chess Club has michael@mergington.edu and daniel@mergington.edu
    
    # Unregister michael
    response = client.post(
        "/activities/Chess%20Club/unregister?email=michael@mergington.edu"
    )
    assert response.status_code == 200
    
    # Check that only michael was removed
    response = client.get("/activities")
    participants = response.json()["Chess Club"]["participants"]
    assert "michael@mergington.edu" not in participants
    assert "daniel@mergington.edu" in participants
    assert len(participants) == 1
