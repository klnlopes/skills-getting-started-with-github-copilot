"""
Step Tracker Module for GitHub Copilot Assessment

This module manages tracking of assessment steps completion for the
"Getting Started with GitHub Copilot" exercise.
"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel


class StepInfo(BaseModel):
    """Information about a single assessment step"""
    step_id: str
    step_number: int
    title: str
    description: str
    completed: bool = False
    completed_at: Optional[datetime] = None


class StepProgress(BaseModel):
    """Overall progress tracking"""
    total_steps: int
    completed_steps: int
    percentage: float
    current_step: Optional[str] = None


# Define the assessment steps based on .github/steps/ directory
ASSESSMENT_STEPS = [
    {
        "step_id": "1-preparing",
        "step_number": 1,
        "title": "Hello Copilot",
        "description": "Get a project intro from Copilot Chat and use Copilot to help remember terminal commands"
    },
    {
        "step_id": "2-first-introduction",
        "step_number": 2,
        "title": "Getting work done with Copilot",
        "description": "Use Copilot to fix registration bugs and generate sample data"
    },
    {
        "step_id": "3-copilot-edits",
        "step_number": 3,
        "title": "Getting work done even faster with Copilot Edit Mode",
        "description": "Use Copilot Edit Mode to add new features across multiple files"
    },
    {
        "step_id": "4-copilot-agent-mode",
        "step_number": 4,
        "title": "Engage Hyperdrive - Copilot Agent Mode",
        "description": "Use Copilot Agent Mode to add functional unregister buttons and test coverage"
    },
    {
        "step_id": "5-copilot-on-github",
        "step_number": 5,
        "title": "Using GitHub Copilot within a pull request",
        "description": "Summarize and review a PR with Copilot"
    },
    {
        "step_id": "x-review",
        "step_number": 6,
        "title": "Review",
        "description": "Congratulations! Review all the GitHub Copilot features you learned"
    }
]


class StepTracker:
    """Manages the tracking of assessment step completion"""
    
    def __init__(self):
        """Initialize the step tracker with default steps"""
        self.steps: Dict[str, StepInfo] = {}
        for step_data in ASSESSMENT_STEPS:
            self.steps[step_data["step_id"]] = StepInfo(**step_data)
    
    def get_all_steps(self) -> List[StepInfo]:
        """Get all assessment steps in order"""
        return sorted(self.steps.values(), key=lambda x: x.step_number)
    
    def get_step(self, step_id: str) -> Optional[StepInfo]:
        """Get a specific step by ID"""
        return self.steps.get(step_id)
    
    def mark_step_complete(self, step_id: str) -> StepInfo:
        """Mark a step as completed"""
        if step_id not in self.steps:
            raise ValueError(f"Step '{step_id}' not found")
        
        step = self.steps[step_id]
        if not step.completed:
            step.completed = True
            step.completed_at = datetime.now()
        
        return step
    
    def mark_step_incomplete(self, step_id: str) -> StepInfo:
        """Mark a step as incomplete"""
        if step_id not in self.steps:
            raise ValueError(f"Step '{step_id}' not found")
        
        step = self.steps[step_id]
        step.completed = False
        step.completed_at = None
        
        return step
    
    def get_progress(self) -> StepProgress:
        """Get overall progress statistics"""
        all_steps = self.get_all_steps()
        total_steps = len(all_steps)
        completed_steps = sum(1 for step in all_steps if step.completed)
        percentage = (completed_steps / total_steps * 100) if total_steps > 0 else 0
        
        # Find the current (first incomplete) step
        current_step = None
        for step in all_steps:
            if not step.completed:
                current_step = step.step_id
                break
        
        return StepProgress(
            total_steps=total_steps,
            completed_steps=completed_steps,
            percentage=round(percentage, 2),
            current_step=current_step
        )
    
    def reset_all_steps(self) -> None:
        """Reset all steps to incomplete"""
        for step in self.steps.values():
            step.completed = False
            step.completed_at = None


# Global step tracker instance
step_tracker = StepTracker()
