"""
Tests for the signup endpoint.
"""
import pytest


def test_signup_for_activity_success(client):
    """Test successful signup for an activity."""
    response = client.post(
        "/activities/Basketball%20Team/signup?email=newstudent@mergington.edu"
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    assert "Basketball Team" in data["message"]


def test_signup_adds_participant(client):
    """Test that signup adds participant to the activity."""
    # Get initial participants
    response = client.get("/activities")
    initial_count = len(response.json()["Basketball Team"]["participants"])
    
    # Sign up new participant
    client.post("/activities/Basketball%20Team/signup?email=newstudent@mergington.edu")
    
    # Check that participant was added
    response = client.get("/activities")
    final_count = len(response.json()["Basketball Team"]["participants"])
    assert final_count == initial_count + 1
    assert "newstudent@mergington.edu" in response.json()["Basketball Team"]["participants"]


def test_signup_duplicate_email_fails(client):
    """Test that signing up the same email twice fails."""
    email = "test@mergington.edu"
    
    # First signup should succeed
    response = client.post(f"/activities/Basketball%20Team/signup?email={email}")
    assert response.status_code == 200
    
    # Second signup with same email should fail
    response = client.post(f"/activities/Basketball%20Team/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_nonexistent_activity_fails(client):
    """Test that signing up for a non-existent activity fails."""
    response = client.post(
        "/activities/Nonexistent%20Activity/signup?email=test@mergington.edu"
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_with_existing_participant(client):
    """Test that existing participants cannot sign up again."""
    response = client.post(
        "/activities/Chess%20Club/signup?email=michael@mergington.edu"
    )
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_multiple_different_participants(client):
    """Test that multiple different participants can sign up."""
    emails = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]
    
    for email in emails:
        response = client.post(f"/activities/Basketball%20Team/signup?email={email}")
        assert response.status_code == 200
    
    # Verify all were added
    response = client.get("/activities")
    participants = response.json()["Basketball Team"]["participants"]
    assert len(participants) == 3
    for email in emails:
        assert email in participants
