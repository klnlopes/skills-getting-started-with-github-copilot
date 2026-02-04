// Assessment Step Tracker JavaScript

const API_BASE = '';

// Load and display all steps
async function loadSteps() {
    try {
        const response = await fetch(`${API_BASE}/steps`);
        const steps = await response.json();
        displaySteps(steps);
        await loadProgress();
    } catch (error) {
        console.error('Error loading steps:', error);
        showError('Failed to load steps');
    }
}

// Load and display progress
async function loadProgress() {
    try {
        const response = await fetch(`${API_BASE}/steps/progress/summary`);
        const progress = await response.json();
        displayProgress(progress);
    } catch (error) {
        console.error('Error loading progress:', error);
    }
}

// Display steps in the UI
function displaySteps(steps) {
    const stepsList = document.getElementById('steps-list');
    stepsList.innerHTML = '';

    steps.forEach(step => {
        const stepCard = createStepCard(step);
        stepsList.appendChild(stepCard);
    });
}

// Create a step card element
function createStepCard(step) {
    const card = document.createElement('div');
    card.className = `step-card ${step.completed ? 'completed' : ''}`;
    card.dataset.stepId = step.step_id;

    const completionTime = step.completed_at 
        ? `<div class="completion-time">Completed: ${new Date(step.completed_at).toLocaleString()}</div>`
        : '';

    card.innerHTML = `
        <div class="step-card-header">
            <div class="step-number">${step.completed ? '' : step.step_number}</div>
            <div class="step-title">
                <h3>${step.title}</h3>
            </div>
            <div class="step-status">
                <span class="status-badge ${step.completed ? 'completed' : 'pending'}">
                    ${step.completed ? 'Completed' : 'Pending'}
                </span>
            </div>
        </div>
        <div class="step-description">${step.description}</div>
        ${completionTime}
    `;

    card.addEventListener('click', () => toggleStepCompletion(step.step_id, !step.completed));

    return card;
}

// Display progress bar
function displayProgress(progress) {
    const progressFill = document.getElementById('progress-fill');
    const progressText = document.getElementById('progress-text');
    const stepsCount = document.getElementById('steps-count');

    progressFill.style.width = `${progress.percentage}%`;
    progressText.textContent = `${progress.percentage}%`;
    stepsCount.textContent = `${progress.completed_steps}/${progress.total_steps} steps completed`;

    // Display current step if exists
    displayCurrentStep(progress.current_step);
}

// Display the current step
async function displayCurrentStep(currentStepId) {
    const currentStepSection = document.getElementById('current-step-section');
    const currentStepInfo = document.getElementById('current-step-info');

    if (!currentStepId) {
        currentStepSection.style.display = 'none';
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/steps/${currentStepId}`);
        const step = await response.json();

        currentStepSection.style.display = 'block';
        currentStepInfo.innerHTML = `
            <h4>Step ${step.step_number}: ${step.title}</h4>
            <p>${step.description}</p>
        `;
    } catch (error) {
        console.error('Error loading current step:', error);
        currentStepSection.style.display = 'none';
    }
}

// Toggle step completion status
async function toggleStepCompletion(stepId, completed) {
    try {
        const endpoint = completed ? 'complete' : 'incomplete';
        const response = await fetch(`${API_BASE}/steps/${stepId}/${endpoint}`, {
            method: 'POST'
        });

        if (response.ok) {
            await loadSteps();
            showSuccess(completed ? 'Step marked as completed!' : 'Step marked as incomplete');
        } else {
            throw new Error('Failed to update step');
        }
    } catch (error) {
        console.error('Error toggling step:', error);
        showError('Failed to update step status');
    }
}

// Reset all steps
async function resetAllSteps() {
    if (!confirm('Are you sure you want to reset all steps? This will mark all steps as incomplete.')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/steps/reset`, {
            method: 'POST'
        });

        if (response.ok) {
            await loadSteps();
            showSuccess('All steps have been reset');
        } else {
            throw new Error('Failed to reset steps');
        }
    } catch (error) {
        console.error('Error resetting steps:', error);
        showError('Failed to reset steps');
    }
}

// Show success message
function showSuccess(message) {
    showNotification(message, 'success');
}

// Show error message
function showError(message) {
    showNotification(message, 'error');
}

// Show notification
function showNotification(message, type) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? '#2da44e' : '#d1242f'};
        color: white;
        border-radius: 6px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;

    document.body.appendChild(notification);

    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Initialize the tracker
document.addEventListener('DOMContentLoaded', () => {
    loadSteps();

    // Set up reset button
    const resetBtn = document.getElementById('reset-btn');
    resetBtn.addEventListener('click', resetAllSteps);
});
