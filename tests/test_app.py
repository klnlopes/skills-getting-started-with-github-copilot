"""
Tests for the Mergington High School API
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
from src.step_tracker import step_tracker


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before each test"""
    # Store original participants
    original_participants = {
        name: details["participants"].copy()
        for name, details in activities.items()
    }
    yield
    # Restore original participants after test
    for name, participants in original_participants.items():
        activities[name]["participants"] = participants


@pytest.fixture(autouse=True)
def reset_step_tracker():
    """Reset step tracker to initial state before each test"""
    step_tracker.reset_all_steps()
    yield
    step_tracker.reset_all_steps()


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_activities_returns_all_activities(self, client):
        """Test that all activities are returned"""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data

    def test_get_activities_returns_correct_structure(self, client):
        """Test that activities have the correct structure"""
        response = client.get("/activities")
        data = response.json()
        chess_club = data["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club


class TestSignup:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_success(self, client):
        """Test successful signup for an activity"""
        response = client.post(
            "/activities/Chess Club/signup?email=newstudent@mergington.edu"
        )
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]

    def test_signup_activity_not_found(self, client):
        """Test signup for non-existent activity"""
        response = client.post(
            "/activities/Nonexistent Activity/signup?email=test@mergington.edu"
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_adds_participant_to_list(self, client):
        """Test that signup actually adds the participant"""
        email = "participant@mergington.edu"
        initial_count = len(activities["Programming Class"]["participants"])
        
        client.post(f"/activities/Programming Class/signup?email={email}")
        
        assert len(activities["Programming Class"]["participants"]) == initial_count + 1
        assert email in activities["Programming Class"]["participants"]


class TestUnregister:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint"""

    def test_unregister_success(self, client):
        """Test successful unregistration from an activity"""
        # First ensure the participant exists
        email = "michael@mergington.edu"
        assert email in activities["Chess Club"]["participants"]
        
        response = client.delete(
            f"/activities/Chess Club/unregister?email={email}"
        )
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        assert email not in activities["Chess Club"]["participants"]

    def test_unregister_activity_not_found(self, client):
        """Test unregister from non-existent activity"""
        response = client.delete(
            "/activities/Nonexistent Activity/unregister?email=test@mergington.edu"
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_unregister_student_not_registered(self, client):
        """Test unregister when student is not registered"""
        response = client.delete(
            "/activities/Chess Club/unregister?email=notregistered@mergington.edu"
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Student not registered for this activity"

    def test_unregister_removes_participant_from_list(self, client):
        """Test that unregister actually removes the participant"""
        email = "daniel@mergington.edu"
        initial_count = len(activities["Chess Club"]["participants"])
        
        client.delete(f"/activities/Chess Club/unregister?email={email}")
        
        assert len(activities["Chess Club"]["participants"]) == initial_count - 1
        assert email not in activities["Chess Club"]["participants"]


class TestRootRedirect:
    """Tests for GET / endpoint"""

    def test_root_redirects_to_static(self, client):
        """Test that root redirects to static index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestStepTrackerEndpoints:
    """Tests for step tracker API endpoints"""

    def test_get_all_steps(self, client):
        """Test getting all assessment steps"""
        response = client.get("/steps")
        assert response.status_code == 200
        
        steps = response.json()
        assert isinstance(steps, list)
        assert len(steps) == 6  # 5 regular steps + 1 review step
        
        # Verify step structure
        first_step = steps[0]
        assert "step_id" in first_step
        assert "step_number" in first_step
        assert "title" in first_step
        assert "description" in first_step
        assert "completed" in first_step

    def test_get_specific_step(self, client):
        """Test getting a specific step by ID"""
        response = client.get("/steps/1-preparing")
        assert response.status_code == 200
        
        step = response.json()
        assert step["step_id"] == "1-preparing"
        assert step["step_number"] == 1
        assert step["title"] == "Hello Copilot"
        assert step["completed"] is False

    def test_get_nonexistent_step(self, client):
        """Test getting a non-existent step"""
        response = client.get("/steps/nonexistent-step")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_mark_step_complete(self, client):
        """Test marking a step as completed"""
        response = client.post("/steps/1-preparing/complete")
        assert response.status_code == 200
        
        step = response.json()
        assert step["completed"] is True
        assert step["completed_at"] is not None

    def test_mark_nonexistent_step_complete(self, client):
        """Test marking a non-existent step as completed"""
        response = client.post("/steps/nonexistent/complete")
        assert response.status_code == 404

    def test_mark_step_incomplete(self, client):
        """Test marking a step as incomplete"""
        # First complete it
        client.post("/steps/1-preparing/complete")
        
        # Then mark it incomplete
        response = client.post("/steps/1-preparing/incomplete")
        assert response.status_code == 200
        
        step = response.json()
        assert step["completed"] is False
        assert step["completed_at"] is None

    def test_get_progress_summary(self, client):
        """Test getting progress summary"""
        response = client.get("/steps/progress/summary")
        assert response.status_code == 200
        
        progress = response.json()
        assert "total_steps" in progress
        assert "completed_steps" in progress
        assert "percentage" in progress
        assert "current_step" in progress
        
        assert progress["total_steps"] == 6
        assert progress["completed_steps"] == 0
        assert progress["percentage"] == 0.0
        assert progress["current_step"] == "1-preparing"

    def test_progress_after_completing_steps(self, client):
        """Test progress updates after completing steps"""
        # Complete two steps
        client.post("/steps/1-preparing/complete")
        client.post("/steps/2-first-introduction/complete")
        
        response = client.get("/steps/progress/summary")
        progress = response.json()
        
        assert progress["completed_steps"] == 2
        assert progress["percentage"] > 0
        assert progress["current_step"] == "3-copilot-edits"

    def test_reset_all_steps(self, client):
        """Test resetting all steps"""
        # Complete some steps
        client.post("/steps/1-preparing/complete")
        client.post("/steps/2-first-introduction/complete")
        
        # Reset all steps
        response = client.post("/steps/reset")
        assert response.status_code == 200
        assert "reset" in response.json()["message"].lower()
        
        # Verify all steps are incomplete
        response = client.get("/steps")
        steps = response.json()
        assert all(not step["completed"] for step in steps)

    def test_step_completion_workflow(self, client):
        """Test a complete workflow of completing all steps"""
        step_ids = [
            "1-preparing",
            "2-first-introduction",
            "3-copilot-edits",
            "4-copilot-agent-mode",
            "5-copilot-on-github",
            "x-review"
        ]
        
        for i, step_id in enumerate(step_ids, 1):
            # Complete the step
            response = client.post(f"/steps/{step_id}/complete")
            assert response.status_code == 200
            
            # Check progress
            progress_response = client.get("/steps/progress/summary")
            progress = progress_response.json()
            assert progress["completed_steps"] == i
        
        # Verify all completed
        final_progress = client.get("/steps/progress/summary").json()
        assert final_progress["completed_steps"] == 6
        assert final_progress["percentage"] == 100.0
        assert final_progress["current_step"] is None
