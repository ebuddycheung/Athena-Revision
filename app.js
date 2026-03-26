// Athena-Revision - 温習助手

// State
let currentSubject = null;
let currentChapter = null;
let currentQuizType = null;
let currentQuestions = [];
let currentQuestionIndex = 0;
let userAnswers = {};

// 科目與課文數據
const sampleContent = {
    chinese: {
        name: "中文",
        chapters: [
            { id: 1, title: "第一課：詠柳（古詩）", ready: true, file: "p5_unit1_poetry.md" },
        ]
    },
    english: {
        name: "英文",
        chapters: [
            { id: 1, title: "Unit 1: Our Environment", ready: true, file: "p5_unit1_environment.md" },
        ]
    },
    math: {
        name: "數學",
        chapters: [
            { id: 1, title: "第一章：分數", ready: false },
            { id: 2, title: "第二章：小數", ready: false },
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
        const subjectName = sampleContent[currentSubject].name;
        document.getElementById('subject-title').textContent = 
            `📑 選擇 ${subjectName} 課文`;
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
                <p>暫時沒有課文。</p>
                <p>請聯絡 Goblin 加入新課文！</p>
            </div>
        `;
        return;
    }
    
    list.innerHTML = chapters.map(ch => `
        <button class="chapter-btn" data-chapter="${ch.id}">
            ${ch.title}
            <span class="status ${ch.ready ? 'ready' : ''}">
                ${ch.ready ? '✓ 可用' : '⏳ 敬請期待'}
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
    showSection('quiz-taking-section');
    document.getElementById('question-container').innerHTML = 
        '<div class="loading">正在生成題目...</div>';
    
    setTimeout(() => {
        generateSampleQuestions();
        displayQuestion();
    }, 1500);
}

// Generate Sample Questions
function generateSampleQuestions() {
    if (currentSubject === 'chinese') {
        currentQuestions = [
            {
                id: 1,
                text: "《詠柳》的作者是誰？",
                options: ["李白", "賀知章", "杜甫", "王維"],
                answer: 1,
                explanation: "《詠柳》的作者是唐代詩人賀知章。"
            },
            {
                id: 2,
                text: "「二月春風似剪刀」用了什麼修辭手法？",
                options: ["比喻", "擬人", "排比", "對偶"],
                answer: 0,
                explanation: "這句詩把春風比作剪刀，是比喻修辭。"
            },
            {
                id: 3,
                text: "「萬條垂下綠絲絛」中的「絲絛」比喻的是什麼？",
                options: ["柳葉", "柳枝", "絲帶", "春風"],
                answer: 1,
                explanation: "「絲絛」指用絲編成的帶子，比喻下垂的柳枝。"
            }
        ];
    } else if (currentSubject === 'english') {
        currentQuestions = [
            {
                id: 1,
                text: "What is the name of the school in the reading?",
                options: ["Green Primary School", "Blue School", "Happy School", "Clean School"],
                answer: 0,
                explanation: "The school is called Green Primary School."
            },
            {
                id: 2,
                text: "How many 'R's are mentioned in the reading?",
                options: ["Two", "Three", "Four", "Five"],
                answer: 1,
                explanation: "Three 'R's are mentioned: Reduce, Reuse, Recycle."
            },
            {
                id: 3,
                text: "The school won the 'Green School Award'.",
                options: ["True", "False"],
                answer: 0,
                explanation: "Yes, the school won the Green School Award last month."
            }
        ];
    } else {
        currentQuestions = [
            {
                id: 1,
                text: "1/2 + 1/4 = ?",
                options: ["2/6", "3/4", "1/6", "2/4"],
                answer: 1,
                explanation: "1/2 = 2/4, 2/4 + 1/4 = 3/4"
            },
            {
                id: 2,
                text: "以下哪個是分數？",
                options: ["0.5", "1/3", "25%", "2"],
                answer: 1,
                explanation: "1/3 是分數格式。"
            }
        ];
    }
    
    currentQuestionIndex = 0;
    userAnswers = {};
}

// Display Question
function displayQuestion() {
    const q = currentQuestions[currentQuestionIndex];
    const container = document.getElementById('question-container');
    
    document.getElementById('progress').textContent = 
        `第 ${currentQuestionIndex + 1}/${currentQuestions.length} 題`;
    
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
                placeholder="請輸入答案...">
        `;
    }
    
    container.innerHTML = html;
    
    document.getElementById('prev-btn').disabled = currentQuestionIndex === 0;
    
    if (currentQuestionIndex === currentQuestions.length - 1) {
        document.getElementById('next-btn').style.display = 'none';
        document.getElementById('submit-btn').style.display = 'inline-block';
    } else {
        document.getElementById('next-btn').style.display = 'inline-block';
        document.getElementById('submit-btn').style.display = 'none';
    }
    
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
    
    document.getElementById('score').textContent = score;
    document.getElementById('total').textContent = currentQuestions.length;
    
    const percentage = (score / currentQuestions.length) * 100;
    let message = '';
    if (percentage >= 90) message = '🌟 太棒了！';
    else if (percentage >= 70) message = '👍 做得好！';
    else if (percentage >= 50) message = '📚 繼續加油！';
    else message = '💪 多溫習，一定進步！';
    
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
document.querySelector('.exit-btn')?.addEventListener('click', () => {
    showSection('subject-section');
});

console.log('Athena 温習助手 loaded! 👺');
