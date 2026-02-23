"""Tests for the POST /activities/{activity_name}/unregister endpoint."""
import pytest


def test_successful_unregister(client):
    """Test successful unregistration from an activity."""
    # michael@mergington.edu is already registered in Chess Club
    response = client.post(
        "/activities/Chess Club/unregister",
        params={"email": "michael@mergington.edu"}
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "michael@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_unregister_removes_participant(client):
    """Test that unregister actually removes the participant."""
    email = "daniel@mergington.edu"
    activity = "Chess Club"
    
    # Verify participant is there initially
    response_before = client.get("/activities")
    activities_before = response_before.json()
    assert email in activities_before[activity]["participants"]
    
    # Unregister
    client.post(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    # Verify participant was removed
    response_after = client.get("/activities")
    activities_after = response_after.json()
    assert email not in activities_after[activity]["participants"]


def test_unregister_nonexistent_activity_returns_404(client):
    """Test that unregistering from a nonexistent activity returns 404."""
    response = client.post(
        "/activities/Nonexistent Club/unregister",
        params={"email": "alice@mergington.edu"}
    )
    assert response.status_code == 404
    
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unregister_nonexistent_participant_returns_400(client):
    """Test that unregistering a non-member returns 400."""
    response = client.post(
        "/activities/Chess Club/unregister",
        params={"email": "notregistered@mergington.edu"}
    )
    assert response.status_code == 400
    
    data = response.json()
    assert "not registered" in data["detail"]


def test_unregister_from_empty_activity_returns_400(client):
    """Test that unregistering from an activity with no participants returns 400."""
    response = client.post(
        "/activities/Basketball Team/unregister",
        params={"email": "alice@mergington.edu"}
    )
    assert response.status_code == 400
    
    data = response.json()
    assert "not registered" in data["detail"]


def test_unregister_message_format(client):
    """Test that unregister returns a properly formatted message."""
    response = client.post(
        "/activities/Gym Class/unregister",
        params={"email": "john@mergington.edu"}
    )
    
    data = response.json()
    assert "message" in data
    assert "john@mergington.edu" in data["message"]
    assert "Gym Class" in data["message"]
    assert "Unregistered" in data["message"]


def test_unregister_then_signup_again(client):
    """Test that a participant can signup again after unregistering."""
    email = "emma@mergington.edu"
    activity = "Programming Class"
    
    # Unregister
    response_unregister = client.post(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    assert response_unregister.status_code == 200
    
    # Sign up again
    response_signup = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert response_signup.status_code == 200
    
    # Verify participant is registered again
    response_activities = client.get("/activities")
    activities = response_activities.json()
    assert email in activities[activity]["participants"]
