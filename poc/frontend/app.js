// QuizFusion POC - Frontend Application
const API_BASE = 'http://localhost:8000';

// Global state
let currentProblem = null;
let allProblems = [];
let currentMode = 'visual';
let codeEditor = null;

// Initialize application
document.addEventListener('DOMContentLoaded', () => {
    initializeCodeEditor();
    initializeEventListeners();
    loadProblems();
});

// Initialize CodeMirror
function initializeCodeEditor() {
    const textarea = document.getElementById('setupCode');
    codeEditor = CodeMirror.fromTextArea(textarea, {
        mode: 'python',
        theme: 'monokai',
        lineNumbers: true,
        indentUnit: 4,
        tabSize: 4,
        indentWithTabs: false,
        autoCloseBrackets: true
    });
    
    codeEditor.on('change', () => {
        // Auto-save or trigger preview update could go here
    });
}

// Initialize event listeners
function initializeEventListeners() {
    // Mode tabs
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => switchMode(tab.dataset.mode));
    });
    
    // Problem type selector
    document.getElementById('problemType').addEventListener('change', updateFormVisibility);
    
    // Buttons
    document.getElementById('newProblemBtn').addEventListener('click', createNewProblem);
    document.getElementById('saveProblemBtn').addEventListener('click', saveProblem);
    document.getElementById('cancelBtn').addEventListener('click', cancelEdit);
    document.getElementById('runCodeBtn').addEventListener('click', runCode);
    document.getElementById('showVariablesBtn').addEventListener('click', toggleVariables);
    document.getElementById('refreshPreviewBtn').addEventListener('click', refreshPreview);
    document.getElementById('addChoiceBtn').addEventListener('click', addChoice);
    document.getElementById('addQuestionBtn').addEventListener('click', addQuestion);
    
    // Auto-preview on input
    document.getElementById('problemStatement').addEventListener('input', debounce(refreshPreview, 500));
}

// Load problems from API
async function loadProblems() {
    try {
        const response = await fetch(`${API_BASE}/api/problems`);
        if (!response.ok) throw new Error('Failed to load problems');
        
        allProblems = await response.json();
        renderProblemList();
    } catch (error) {
        console.error('Error loading problems:', error);
        document.getElementById('problemList').innerHTML = 
            '<div class="error">Failed to load problems. Make sure the backend is running.</div>';
    }
}

// Render problem list
function renderProblemList() {
    const container = document.getElementById('problemList');
    
    if (allProblems.length === 0) {
        container.innerHTML = '<div class="loading">No problems yet. Create one!</div>';
        return;
    }
    
    container.innerHTML = allProblems.map(problem => `
        <div class="problem-item" onclick="loadProblem(${problem.id})">
            <div class="problem-item-title">${truncate(problem.statement, 50)}</div>
            <div class="problem-item-meta">
                <span>${problem.type.replace('_', ' ')}</span>
                <span>${problem.mode}</span>
            </div>
        </div>
    `).join('');
}

// Load a specific problem
async function loadProblem(id) {
    try {
        console.log(`Loading problem ${id}...`);
        const response = await fetch(`${API_BASE}/api/problems/${id}`);
        console.log(`Response status: ${response.status}`);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: Failed to load problem`);
        }
        
        currentProblem = await response.json();
        console.log('Problem loaded:', currentProblem);
        
        populateForm(currentProblem);
        console.log('Form populated');
        
        await refreshPreview();
        console.log('Preview refreshed');
        
        // Highlight active problem
        document.querySelectorAll('.problem-item').forEach(item => item.classList.remove('active'));
        const clickedItem = document.querySelector(`.problem-item[onclick="loadProblem(${id})"]`);
        if (clickedItem) {
            clickedItem.classList.add('active');
        }
        console.log('Problem loaded successfully');
    } catch (error) {
        console.error('Error loading problem:', error);
        console.error('Error stack:', error.stack);
        alert('Failed to load problem: ' + error.message);
    }
}

// Populate form with problem data
function populateForm(problem) {
    document.getElementById('problemType').value = problem.type;
    document.getElementById('problemTags').value = problem.tags.join(', ');
    document.getElementById('problemTopic').value = problem.topic || '';
    document.getElementById('problemDifficulty').value = problem.difficulty || '';
    document.getElementById('problemStatement').value = problem.statement;
    
    // Switch to appropriate mode
    switchMode(problem.mode);
    
    // Setup code
    if (problem.setup_code) {
        codeEditor.setValue(problem.setup_code);
    } else {
        codeEditor.setValue('');
    }
    
    // Type-specific content
    if (problem.type === 'multiple_choice' && problem.choices) {
        renderChoices(problem.choices);
    } else if (problem.type === 'work' && problem.questions) {
        renderQuestions(problem.questions);
    }
    
    updateFormVisibility();
}

// Switch editor mode
function switchMode(mode) {
    currentMode = mode;
    
    // Update tabs
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.toggle('active', tab.dataset.mode === mode);
    });
    
    // Show/hide setup code section
    const setupCodeSection = document.getElementById('setupCodeSection');
    setupCodeSection.style.display = (mode === 'hybrid' || mode === 'code') ? 'block' : 'none';
    
    // In code mode, hide visual form elements
    if (mode === 'code') {
        document.getElementById('choicesSection').style.display = 'none';
        document.getElementById('questionsSection').style.display = 'none';
    } else {
        updateFormVisibility();
    }
}

// Update form visibility based on problem type
function updateFormVisibility() {
    const type = document.getElementById('problemType').value;
    
    document.getElementById('choicesSection').style.display = 
        type === 'multiple_choice' && currentMode !== 'code' ? 'block' : 'none';
    document.getElementById('questionsSection').style.display = 
        type === 'work' && currentMode !== 'code' ? 'block' : 'none';
}

// Create new problem
function createNewProblem() {
    currentProblem = null;
    
    // Reset form
    document.getElementById('problemType').value = 'multiple_choice';
    document.getElementById('problemTags').value = '';
    document.getElementById('problemTopic').value = '';
    document.getElementById('problemDifficulty').value = '';
    document.getElementById('problemStatement').value = '';
    codeEditor.setValue('');
    
    // Clear choices/questions
    document.getElementById('choicesList').innerHTML = '';
    document.getElementById('questionsList').innerHTML = '';
    
    // Add default items
    addChoice();
    addQuestion();
    
    updateFormVisibility();
    document.getElementById('previewContent').innerHTML = 
        '<div class="preview-placeholder">Configure your problem...</div>';
    
    // Clear active selection
    document.querySelectorAll('.problem-item').forEach(item => item.classList.remove('active'));
}

// Save problem
async function saveProblem() {
    const problemData = gatherFormData();
    
    try {
        const url = currentProblem 
            ? `${API_BASE}/api/problems/${currentProblem.id}`
            : `${API_BASE}/api/problems`;
        
        const method = currentProblem ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method,
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(problemData)
        });
        
        if (!response.ok) throw new Error('Failed to save problem');
        
        const saved = await response.json();
        currentProblem = saved;
        
        // Reload problem list
        await loadProblems();
        alert('Problem saved successfully!');
    } catch (error) {
        console.error('Error saving problem:', error);
        alert('Failed to save problem');
    }
}

// Gather form data
function gatherFormData() {
    const tags = document.getElementById('problemTags').value
        .split(',')
        .map(t => t.trim())
        .filter(t => t);
    
    const data = {
        type: document.getElementById('problemType').value,
        mode: currentMode,
        statement: document.getElementById('problemStatement').value,
        setup_code: codeEditor.getValue() || null,
        tags,
        topic: document.getElementById('problemTopic').value || null,
        difficulty: document.getElementById('problemDifficulty').value || null,
        choices: null,
        questions: null,
        extras: null
    };
    
    // Add type-specific data
    if (data.type === 'multiple_choice') {
        data.choices = gatherChoices();
    } else if (data.type === 'work') {
        data.questions = gatherQuestions();
    }
    
    return data;
}

// Cancel edit
function cancelEdit() {
    if (confirm('Discard changes?')) {
        if (currentProblem) {
            populateForm(currentProblem);
        } else {
            createNewProblem();
        }
    }
}

// Run code and show output
async function runCode() {
    const code = codeEditor.getValue();
    const outputDiv = document.getElementById('codeOutput');
    
    if (!code.trim()) {
        alert('No code to run');
        return;
    }
    
    outputDiv.style.display = 'block';
    outputDiv.innerHTML = '<div class="loading">Executing code...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/api/execute`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ code, timeout: 5 })
        });
        
        if (!response.ok) throw new Error('Execution failed');
        
        const result = await response.json();
        
        if (result.success) {
            outputDiv.classList.remove('error');
            outputDiv.innerHTML = '<strong>✓ Code executed successfully</strong><br>' +
                '<pre>' + JSON.stringify(result.namespace, null, 2) + '</pre>';
            
            // Auto-refresh preview
            refreshPreview();
        } else {
            outputDiv.classList.add('error');
            outputDiv.innerHTML = '<strong>✗ Execution error:</strong><br>' +
                '<pre>' + result.error + '</pre>';
        }
    } catch (error) {
        outputDiv.classList.add('error');
        outputDiv.innerHTML = '<strong>✗ Error:</strong><br>' + error.message;
    }
}

// Toggle variables display
function toggleVariables() {
    const varsDisplay = document.getElementById('variablesDisplay');
    varsDisplay.style.display = varsDisplay.style.display === 'none' ? 'block' : 'none';
}

// Refresh preview
async function refreshPreview() {
    console.log('refreshPreview called');
    const problemData = gatherFormData();
    console.log('Form data gathered:', problemData);
    const previewDiv = document.getElementById('previewContent');
    
    try {
        const response = await fetch(`${API_BASE}/api/preview`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ problem: problemData })
        });
        
        console.log(`Preview response status: ${response.status}`);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('Preview request failed:', errorText);
            throw new Error('Preview failed');
        }
        
        const result = await response.json();
        console.log('Preview result:', result);
        
        if (result.error) {
            console.error('Preview generation error:', result.error);
            previewDiv.innerHTML = `<div class="error">${result.error}</div>`;
        } else {
            previewDiv.innerHTML = result.html;
            
            // Show variables
            const varsDiv = document.getElementById('variablesList');
            if (Object.keys(result.namespace).length > 0) {
                varsDiv.innerHTML = Object.entries(result.namespace).map(([key, value]) => {
                    const display = value.formatted || JSON.stringify(value);
                    return `<div class="variable-item">
                        <span class="variable-name">${key}:</span> ${display}
                    </div>`;
                }).join('');
            }
        }
    } catch (error) {
        console.error('Preview error:', error);
        console.error('Error stack:', error.stack);
        previewDiv.innerHTML = `<div class="error">Preview error: ${error.message}</div>`;
    }
}

// Choices management
function addChoice() {
    const container = document.getElementById('choicesList');
    const choiceId = Date.now();
    
    const choiceHTML = `
        <div class="choice-item" data-id="${choiceId}">
            <div class="choice-item-header">
                <label><input type="checkbox" class="choice-correct"> Correct Answer</label>
                <button class="btn btn-small btn-danger" onclick="removeChoice(${choiceId})">×</button>
            </div>
            <input type="text" class="choice-text" placeholder="Choice statement">
        </div>
    `;
    
    container.insertAdjacentHTML('beforeend', choiceHTML);
}

function removeChoice(id) {
    document.querySelector(`.choice-item[data-id="${id}"]`).remove();
}

function gatherChoices() {
    return Array.from(document.querySelectorAll('.choice-item')).map(item => ({
        statement: item.querySelector('.choice-text').value,
        correct: item.querySelector('.choice-correct').checked
    }));
}

function renderChoices(choices) {
    const container = document.getElementById('choicesList');
    container.innerHTML = '';
    
    choices.forEach(choice => {
        addChoice();
        const lastChoice = container.lastElementChild;
        lastChoice.querySelector('.choice-text').value = choice.statement;
        lastChoice.querySelector('.choice-correct').checked = choice.correct;
    });
}

// Questions management
function addQuestion() {
    const container = document.getElementById('questionsList');
    const questionId = Date.now();
    
    const questionHTML = `
        <div class="question-item" data-id="${questionId}">
            <div class="question-item-header">
                <label>Question</label>
                <button class="btn btn-small btn-danger" onclick="removeQuestion(${questionId})">×</button>
            </div>
            <textarea class="question-text" rows="2" placeholder="Question statement"></textarea>
            <div class="question-item-controls">
                <input type="number" class="question-points" value="3" min="1" max="20" placeholder="Points">
                <input type="number" class="question-space" value="10" min="1" max="50" placeholder="Lines">
            </div>
        </div>
    `;
    
    container.insertAdjacentHTML('beforeend', questionHTML);
}

function removeQuestion(id) {
    document.querySelector(`.question-item[data-id="${id}"]`).remove();
}

function gatherQuestions() {
    return Array.from(document.querySelectorAll('.question-item')).map(item => ({
        statement: item.querySelector('.question-text').value,
        points: parseInt(item.querySelector('.question-points').value) || 3,
        space: parseInt(item.querySelector('.question-space').value) || 10
    }));
}

function renderQuestions(questions) {
    const container = document.getElementById('questionsList');
    container.innerHTML = '';
    
    questions.forEach(question => {
        addQuestion();
        const lastQuestion = container.lastElementChild;
        lastQuestion.querySelector('.question-text').value = question.statement;
        lastQuestion.querySelector('.question-points').value = question.points;
        lastQuestion.querySelector('.question-space').value = question.space;
    });
}

// Utility functions
function truncate(str, length) {
    return str.length > length ? str.substring(0, length) + '...' : str;
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
