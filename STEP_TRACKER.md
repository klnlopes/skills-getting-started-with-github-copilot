# Assessment Step Tracker

## Overview

The Assessment Step Tracker is a comprehensive system for tracking progress through the "Getting Started with GitHub Copilot" exercise. It provides both a REST API and a web interface to manage and visualize step completion.

## Features

- **Track 6 Assessment Steps**: Monitor progress through all exercise steps
- **Visual Progress Bar**: See completion percentage at a glance
- **Interactive Step Cards**: Click to mark steps as complete/incomplete
- **Current Step Indicator**: Highlights which step you should work on next
- **Persistent State**: Step completion is maintained during the session
- **REST API**: Full programmatic access to step tracking functionality

## Steps Tracked

1. **Hello Copilot** - Get a project intro from Copilot Chat
2. **Getting work done with Copilot** - Use Copilot to fix bugs and generate data
3. **Edit Mode** - Use Copilot Edit Mode for multi-file changes
4. **Agent Mode** - Use Copilot Agent Mode for autonomous editing
5. **Copilot on GitHub** - Use Copilot for PR summaries and reviews
6. **Review** - Complete the exercise and review what you learned

## Web Interface

### Access the Tracker

Navigate to `/static/tracker.html` in your browser to access the step tracker interface.

From the main activities page, click the "📊 Assessment Step Tracker" link in the header.

### Using the Interface

- **View Progress**: See your overall completion percentage and current step
- **Complete Steps**: Click on any step card to toggle its completion status
- **Reset Progress**: Use the "Reset All Steps" button to start over
- **Navigate**: Use "Back to Activities" to return to the main page

## API Reference

### Get All Steps

```http
GET /steps
```

Returns all assessment steps in order.

**Response:**
```json
[
  {
    "step_id": "1-preparing",
    "step_number": 1,
    "title": "Hello Copilot",
    "description": "Get a project intro from Copilot Chat and use Copilot to help remember terminal commands",
    "completed": false,
    "completed_at": null
  },
  ...
]
```

### Get Specific Step

```http
GET /steps/{step_id}
```

Returns details for a specific step.

**Parameters:**
- `step_id` (string): Step identifier (e.g., "1-preparing")

**Response:**
```json
{
  "step_id": "1-preparing",
  "step_number": 1,
  "title": "Hello Copilot",
  "description": "Get a project intro from Copilot Chat and use Copilot to help remember terminal commands",
  "completed": false,
  "completed_at": null
}
```

### Mark Step as Complete

```http
POST /steps/{step_id}/complete
```

Marks a step as completed.

**Parameters:**
- `step_id` (string): Step identifier

**Response:**
```json
{
  "step_id": "1-preparing",
  "step_number": 1,
  "title": "Hello Copilot",
  "description": "Get a project intro from Copilot Chat and use Copilot to help remember terminal commands",
  "completed": true,
  "completed_at": "2024-02-04T21:30:00.123456"
}
```

### Mark Step as Incomplete

```http
POST /steps/{step_id}/incomplete
```

Marks a step as incomplete.

**Parameters:**
- `step_id` (string): Step identifier

**Response:**
```json
{
  "step_id": "1-preparing",
  "step_number": 1,
  "title": "Hello Copilot",
  "description": "Get a project intro from Copilot Chat and use Copilot to help remember terminal commands",
  "completed": false,
  "completed_at": null
}
```

### Get Progress Summary

```http
GET /steps/progress/summary
```

Returns overall progress statistics.

**Response:**
```json
{
  "total_steps": 6,
  "completed_steps": 2,
  "percentage": 33.33,
  "current_step": "3-copilot-edits"
}
```

### Reset All Steps

```http
POST /steps/reset
```

Resets all steps to incomplete status.

**Response:**
```json
{
  "message": "All steps have been reset"
}
```

## Implementation Details

### Architecture

The step tracker consists of three main components:

1. **Step Tracker Module** (`src/step_tracker.py`): Core business logic
2. **API Endpoints** (`src/app.py`): REST API integration
3. **Web Interface** (`src/static/tracker.html`, `tracker.js`, `tracker.css`): User interface

### Data Model

#### StepInfo
Represents a single assessment step with the following fields:
- `step_id`: Unique identifier
- `step_number`: Step order (1-6)
- `title`: Step name
- `description`: Brief description of what the step involves
- `completed`: Boolean completion status
- `completed_at`: Timestamp of completion (nullable)

#### StepProgress
Represents overall progress with:
- `total_steps`: Total number of steps
- `completed_steps`: Number of completed steps
- `percentage`: Completion percentage
- `current_step`: ID of the first incomplete step (nullable)

### State Management

The step tracker maintains in-memory state during the application session. To persist state across sessions, you would need to add a database backend.

## Usage Example

### Using the API with curl

```bash
# Get all steps
curl http://localhost:8000/steps

# Get progress
curl http://localhost:8000/steps/progress/summary

# Mark step 1 as complete
curl -X POST http://localhost:8000/steps/1-preparing/complete

# Mark step 1 as incomplete
curl -X POST http://localhost:8000/steps/1-preparing/incomplete

# Reset all steps
curl -X POST http://localhost:8000/steps/reset
```

### Using the API with JavaScript

```javascript
// Get all steps
const steps = await fetch('/steps').then(r => r.json());

// Mark a step complete
await fetch('/steps/1-preparing/complete', { method: 'POST' });

// Get progress
const progress = await fetch('/steps/progress/summary').then(r => r.json());
console.log(`${progress.percentage}% complete`);
```

## Development

### Running Tests

```bash
# Run all tests
pytest tests/

# Run step tracker tests only
pytest tests/test_step_tracker.py

# Run with verbose output
pytest tests/ -v
```

### Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the development server
uvicorn src.app:app --reload --port 8000
```

Then navigate to:
- Activities page: http://localhost:8000/
- Step tracker: http://localhost:8000/static/tracker.html

## Future Enhancements

Potential improvements for the step tracker:

1. **Persistence**: Add database support for permanent storage
2. **User Accounts**: Track progress per user
3. **Step Details**: Link to step documentation from the tracker
4. **Achievements**: Add badges or rewards for completing steps
5. **Time Tracking**: Record how long each step took
6. **Analytics**: Generate progress reports and statistics
7. **Export**: Allow exporting progress as PDF or CSV

## License

MIT License - See LICENSE file for details
