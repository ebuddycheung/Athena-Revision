// Athena-Revision - Frontend Logic

// State
let currentSubject = null;
let currentChapter = null;
let currentQuizType = null;
let currentQuestions = [];
let currentQuestionIndex = 0;
let userAnswers = {};

// Sample data for demonstration
const sampleContent = {
    science: {
        chapters: [
            { id: 1, title: "Introduction to Biology", ready: false },
            { id: 2, title: "Cell Structure", ready: false },
            { id: 3, title: "Photosynthesis", ready: false },
        ]
    },
    math: {
        chapters: [
            { id: 1, title: "Algebra Basics", ready: false },
            { id: 2, title: "Geometry", ready: false },
        ]
    },
    english: {
        chapters: [
            { id: 1, title: "Our Environment (Unit 1)", ready: true, file: "p5_unit1_environment.md" },
            { id: 2, title: "Grammar Fundamentals", ready: false },
        ]
    },
    chinese: {
        chapters: [
            { id: 1, title: "古詩朗讀《詠柳》", ready: true, file: "p5_unit1_poetry.md" },
            { id: 2, title: "詞語學習", ready: false },
        ]
    },
    history: {
        chapters: [
            { id: 1, title: "Ancient Civilizations", ready: false },
        ]
    },
    geography: {
        chapters: [
            { id: 1, title: "World Regions", ready: false },
        ]
    },
    other: {
        chapters: [
            { id: 1, title: "General Knowledge", ready: false },
        ]
    }
};

// Navigation
function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.getElementById(sectionId).classList.add('active');
}

// Subject Selection
document.querySelectorAll('.subject-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        currentSubject = btn.dataset.subject;
        document.getElementById('subject-title').textContent = 
            `📑 Select ${btn.textContent} Chapter`;
        populateChapters();
        showSection('chapter-section');
    });
});

// Populate Chapters
function populateChapters() {
    const list = document.getElementById('chapter-list');
    const chapters = sampleContent[currentSubject]?.chapters || [];
    
    if (chapters.length === 0) {
        list.innerHTML = `
            <div class="empty-state">
                <div class="icon">📚</div>
                <p>No chapters available yet.</p>
                <p>Ask Goblin to add content for this subject!</p>
            </div>
        `;
        return;
    }
    
    list.innerHTML = chapters.map(ch => `
        <button class="chapter-btn" data-chapter="${ch.id}">
            Chapter ${ch.id}: ${ch.title}
            <span class="status ${ch.ready ? 'ready' : ''}">
                ${ch.ready ? '✓ Ready' : '⏳ Coming soon'}
            </span>
        </button>
    `).join('');
    
    list.querySelectorAll('.chapter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            if (btn.querySelector('.status').classList.contains('ready')) {
                currentChapter = btn.dataset.chapter;
                showSection('quiz-section');
            }
        });
    });
}

// Quiz Type Selection
document.querySelectorAll('.quiz-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        currentQuizType = btn.dataset.type;
        startQuiz();
    });
});

// Start Quiz
function startQuiz() {
    // Show loading
    showSection('quiz-taking-section');
    document.getElementById('question-container').innerHTML = 
        '<div class="loading">Generating questions</div>';
    
    // Simulate loading (in real app, this would call the API)
    setTimeout(() => {
        generateSampleQuestions();
        displayQuestion();
    }, 1500);
}

// Generate Sample Questions (placeholder)
function generateSampleQuestions() {
    // This would be replaced by AI-generated questions from Goblin
    currentQuestions = [
        {
            id: 1,
            text: "What is the basic unit of life?",
            options: ["Atom", "Cell", "Molecule", "Organ"],
            answer: 1,
            explanation: "The cell is the basic structural and functional unit of all living organisms."
        },
        {
            id: 2,
            text: "Cells with a nucleus are called prokaryotic cells.",
            options: ["True", "False"],
            answer: 1,
            explanation: "Cells with a nucleus are called eukaryotic cells. Prokaryotic cells do not have a nucleus."
        },
        {
            id: 3,
            text: "Fill in the blank: The process by which plants make food is called _____.",
            answer: "Photosynthesis",
            explanation: "Photosynthesis is the process by which plants convert light energy into chemical energy."
        }
    ];
    
    currentQuestionIndex = 0;
    userAnswers = {};
}

// Display Question
function displayQuestion() {
    const q = currentQuestions[currentQuestionIndex];
    const container = document.getElementById('question-container');
    
    document.getElementById('progress').textContent = 
        `Question ${currentQuestionIndex + 1}/${currentQuestions.length}`;
    
    let html = `<p class="question-text">${q.text}</p>`;
    
    if (q.options) {
        html += '<div class="options">';
        q.options.forEach((opt, i) => {
            html += `
                <label class="option ${userAnswers[q.id] === i ? 'selected' : ''}">
                    <input type="radio" name="answer" value="${i}" 
                        ${userAnswers[q.id] === i ? 'checked' : ''}>
                    ${opt}
                </label>
            `;
        });
        html += '</div>';
    } else {
        html += `
            <input type="text" class="fill-input" 
                value="${userAnswers[q.id] || ''}" 
                placeholder="Type your answer...">
        `;
    }
    
    container.innerHTML = html;
    
    // Update navigation buttons
    document.getElementById('prev-btn').disabled = currentQuestionIndex === 0;
    
    if (currentQuestionIndex === currentQuestions.length - 1) {
        document.getElementById('next-btn').style.display = 'none';
        document.getElementById('submit-btn').style.display = 'inline-block';
    } else {
        document.getElementById('next-btn').style.display = 'inline-block';
        document.getElementById('submit-btn').style.display = 'none';
    }
    
    // Add event listeners
    container.querySelectorAll('input[name="answer"]').forEach(input => {
        input.addEventListener('change', (e) => {
            userAnswers[q.id] = parseInt(e.target.value);
            displayQuestion();
        });
    });
    
    const fillInput = container.querySelector('.fill-input');
    if (fillInput) {
        fillInput.addEventListener('input', (e) => {
            userAnswers[q.id] = e.target.value;
        });
    }
}

// Navigation
document.getElementById('prev-btn').addEventListener('click', () => {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        displayQuestion();
    }
});

document.getElementById('next-btn').addEventListener('click', () => {
    if (currentQuestionIndex < currentQuestions.length - 1) {
        currentQuestionIndex++;
        displayQuestion();
    }
});

document.getElementById('submit-btn').addEventListener('click', submitQuiz);

function submitQuiz() {
    // Calculate score
    let score = 0;
    currentQuestions.forEach(q => {
        if (q.options) {
            if (userAnswers[q.id] === q.answer) score++;
        } else {
            if (userAnswers[q.id]?.toLowerCase().trim() === q.answer.toLowerCase().trim()) {
                score++;
            }
        }
    });
    
    // Show results
    document.getElementById('score').textContent = score;
    document.getElementById('total').textContent = currentQuestions.length;
    
    const percentage = (score / currentQuestions.length) * 100;
    let message = '';
    if (percentage >= 90) message = '🌟 Excellent!';
    else if (percentage >= 70) message = '👍 Good job!';
    else if (percentage >= 50) message = '📚 Keep practicing!';
    else message = '💪 You can do better!';
    
    document.getElementById('score-message').textContent = message;
    showSection('results-section');
}

function restartQuiz() {
    startQuiz();
}

function goHome() {
    showSection('subject-section');
}

// Back buttons
document.querySelectorAll('.back-btn')[0]?.addEventListener('click', () => {
    showSection('subject-section');
});
document.querySelectorAll('.back-btn')[1]?.addEventListener('click', () => {
    showSection('chapter-section');
});
document.querySelectorAll('.back-btn')[2]?.addEventListener('click', () => {
    showSection('quiz-section');
});

// Initialize
console.log('Athena-Revision loaded! 👺');
