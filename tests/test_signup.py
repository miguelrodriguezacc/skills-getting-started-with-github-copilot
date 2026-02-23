"""Tests for the POST /activities/{activity_name}/signup endpoint."""
import pytest


def test_successful_signup(client):
    """Test successful signup for an activity."""
    response = client.post(
        "/activities/Basketball Team/signup",
        params={"email": "alice@mergington.edu"}
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "alice@mergington.edu" in data["message"]
    assert "Basketball Team" in data["message"]


def test_signup_adds_participant_to_activity(client):
    """Test that signup actually adds the participant to the activity."""
    # Signup
    client.post(
        "/activities/Tennis Club/signup",
        params={"email": "bob@mergington.edu"}
    )
    
    # Verify participant was added
    response = client.get("/activities")
    activities = response.json()
    assert "bob@mergington.edu" in activities["Tennis Club"]["participants"]


def test_signup_nonexistent_activity_returns_404(client):
    """Test that signing up for a nonexistent activity returns 404."""
    response = client.post(
        "/activities/Nonexistent Club/signup",
        params={"email": "alice@mergington.edu"}
    )
    assert response.status_code == 404
    
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_duplicate_signup_returns_400(client):
    """Test that signing up twice for the same activity returns 400."""
    email = "charlie@mergington.edu"
    activity = "Drama Club"
    
    # First signup should succeed
    response1 = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Second signup with same email should fail
    response2 = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert response2.status_code == 400
    
    data = response2.json()
    assert "already signed up" in data["detail"]


def test_signup_with_existing_participant(client):
    """Test that an already registered participant cannot sign up again."""
    # michael@mergington.edu is already in Chess Club
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"}
    )
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_valid_email_format_signup(client):
    """Test signup with valid email formats."""
    test_emails = [
        "student1@mergington.edu",
        "john.doe@mergington.edu",
        "student_123@mergington.edu"
    ]
    
    for email in test_emails:
        response = client.post(
            "/activities/Art Studio/signup",
            params={"email": email}
        )
        assert response.status_code == 200


def test_signup_message_format(client):
    """Test that signup returns a properly formatted message."""
    response = client.post(
        "/activities/Debate Team/signup",
        params={"email": "david@mergington.edu"}
    )
    
    data = response.json()
    assert "message" in data
    assert "david@mergington.edu" in data["message"]
    assert "Debate Team" in data["message"]
    assert "Signed up" in data["message"]
