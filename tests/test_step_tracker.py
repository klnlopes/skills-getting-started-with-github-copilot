"""
Tests for the Step Tracker Module
"""

import pytest
from datetime import datetime
from src.step_tracker import StepTracker, StepInfo, StepProgress, ASSESSMENT_STEPS


class TestStepTracker:
    """Tests for the StepTracker class"""

    @pytest.fixture
    def tracker(self):
        """Create a fresh step tracker instance for each test"""
        return StepTracker()

    def test_initialization(self, tracker):
        """Test that the tracker initializes with all steps"""
        steps = tracker.get_all_steps()
        assert len(steps) == len(ASSESSMENT_STEPS)
        assert all(isinstance(step, StepInfo) for step in steps)
        assert all(not step.completed for step in steps)

    def test_get_all_steps_ordered(self, tracker):
        """Test that steps are returned in correct order"""
        steps = tracker.get_all_steps()
        step_numbers = [step.step_number for step in steps]
        assert step_numbers == sorted(step_numbers)
        assert step_numbers[0] == 1

    def test_get_step_by_id(self, tracker):
        """Test retrieving a specific step by ID"""
        step = tracker.get_step("1-preparing")
        assert step is not None
        assert step.step_id == "1-preparing"
        assert step.step_number == 1
        assert step.title == "Hello Copilot"

    def test_get_step_invalid_id(self, tracker):
        """Test retrieving a non-existent step"""
        step = tracker.get_step("nonexistent")
        assert step is None

    def test_mark_step_complete(self, tracker):
        """Test marking a step as completed"""
        step_id = "1-preparing"
        step = tracker.mark_step_complete(step_id)
        
        assert step.completed is True
        assert step.completed_at is not None
        assert isinstance(step.completed_at, datetime)

    def test_mark_step_complete_twice(self, tracker):
        """Test that marking a completed step again keeps the original completion time"""
        step_id = "1-preparing"
        
        step1 = tracker.mark_step_complete(step_id)
        first_completion_time = step1.completed_at
        
        step2 = tracker.mark_step_complete(step_id)
        
        assert step2.completed_at == first_completion_time

    def test_mark_step_complete_invalid_id(self, tracker):
        """Test marking a non-existent step as completed"""
        with pytest.raises(ValueError, match="Step 'nonexistent' not found"):
            tracker.mark_step_complete("nonexistent")

    def test_mark_step_incomplete(self, tracker):
        """Test marking a step as incomplete"""
        step_id = "1-preparing"
        
        # First complete it
        tracker.mark_step_complete(step_id)
        
        # Then mark it incomplete
        step = tracker.mark_step_incomplete(step_id)
        
        assert step.completed is False
        assert step.completed_at is None

    def test_mark_step_incomplete_invalid_id(self, tracker):
        """Test marking a non-existent step as incomplete"""
        with pytest.raises(ValueError, match="Step 'nonexistent' not found"):
            tracker.mark_step_incomplete("nonexistent")

    def test_get_progress_no_completion(self, tracker):
        """Test progress when no steps are completed"""
        progress = tracker.get_progress()
        
        assert isinstance(progress, StepProgress)
        assert progress.total_steps == len(ASSESSMENT_STEPS)
        assert progress.completed_steps == 0
        assert progress.percentage == 0.0
        assert progress.current_step == "1-preparing"

    def test_get_progress_partial_completion(self, tracker):
        """Test progress with some steps completed"""
        tracker.mark_step_complete("1-preparing")
        tracker.mark_step_complete("2-first-introduction")
        
        progress = tracker.get_progress()
        
        assert progress.completed_steps == 2
        assert progress.percentage == round(2 / len(ASSESSMENT_STEPS) * 100, 2)
        assert progress.current_step == "3-copilot-edits"

    def test_get_progress_full_completion(self, tracker):
        """Test progress when all steps are completed"""
        for step_data in ASSESSMENT_STEPS:
            tracker.mark_step_complete(step_data["step_id"])
        
        progress = tracker.get_progress()
        
        assert progress.completed_steps == len(ASSESSMENT_STEPS)
        assert progress.percentage == 100.0
        assert progress.current_step is None

    def test_reset_all_steps(self, tracker):
        """Test resetting all steps to incomplete"""
        # Complete some steps
        tracker.mark_step_complete("1-preparing")
        tracker.mark_step_complete("2-first-introduction")
        tracker.mark_step_complete("3-copilot-edits")
        
        # Reset all steps
        tracker.reset_all_steps()
        
        # Verify all steps are incomplete
        steps = tracker.get_all_steps()
        assert all(not step.completed for step in steps)
        assert all(step.completed_at is None for step in steps)
        
        # Verify progress is reset
        progress = tracker.get_progress()
        assert progress.completed_steps == 0
        assert progress.percentage == 0.0

    def test_all_assessment_steps_present(self, tracker):
        """Test that all expected assessment steps are present"""
        expected_step_ids = [
            "1-preparing",
            "2-first-introduction", 
            "3-copilot-edits",
            "4-copilot-agent-mode",
            "5-copilot-on-github",
            "x-review"
        ]
        
        for step_id in expected_step_ids:
            step = tracker.get_step(step_id)
            assert step is not None, f"Step {step_id} should be present"

    def test_step_info_model(self):
        """Test the StepInfo model"""
        step = StepInfo(
            step_id="test-step",
            step_number=1,
            title="Test Step",
            description="Test description",
            completed=True,
            completed_at=datetime.now()
        )
        
        assert step.step_id == "test-step"
        assert step.step_number == 1
        assert step.title == "Test Step"
        assert step.description == "Test description"
        assert step.completed is True
        assert step.completed_at is not None

    def test_step_progress_model(self):
        """Test the StepProgress model"""
        progress = StepProgress(
            total_steps=6,
            completed_steps=3,
            percentage=50.0,
            current_step="3-copilot-edits"
        )
        
        assert progress.total_steps == 6
        assert progress.completed_steps == 3
        assert progress.percentage == 50.0
        assert progress.current_step == "3-copilot-edits"
