"""Tests for the GET /activities endpoint."""
import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities."""
    response = client.get("/activities")
    assert response.status_code == 200
    
    activities = response.json()
    assert len(activities) == 9
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert "Basketball Team" in activities


def test_activity_structure(client):
    """Test that each activity has the required fields."""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        
        # Verify types
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)


def test_initial_participants_present(client):
    """Test that initial participants are correctly included."""
    response = client.get("/activities")
    activities = response.json()
    
    # Chess Club should have 2 participants
    assert len(activities["Chess Club"]["participants"]) == 2
    assert "michael@mergington.edu" in activities["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in activities["Chess Club"]["participants"]
    
    # Programming Class should have 2 participants
    assert len(activities["Programming Class"]["participants"]) == 2
    assert "emma@mergington.edu" in activities["Programming Class"]["participants"]
    
    # Basketball Team should have 0 participants initially
    assert len(activities["Basketball Team"]["participants"]) == 0


def test_activities_have_positive_max_participants(client):
    """Test that all activities have positive max_participants."""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        assert activity_data["max_participants"] > 0


def test_participants_list_does_not_exceed_max(client):
    """Test that participant count doesn't exceed max_participants."""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        assert len(activity_data["participants"]) <= activity_data["max_participants"]
