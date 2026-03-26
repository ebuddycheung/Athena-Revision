// Athena-Revision - 温習助手
// 從題庫隨機讀取題目

// State
let currentSubject = null;
let currentChapter = null;
let currentQuizType = null;
let currentQuestions = [];
let currentQuestionIndex = 0;
let userAnswers = {};

// 科目與課文數據
const subjects = {
    chinese: {
        name: "中文",
        chapters: [
            { id: 1, title: "第一課：詠柳（古詩）", ready: true, file: "chinese_p5_unit1_poetry.json" },
        ]
    },
    english: {
        name: "英文",
        chapters: [
            { id: 1, title: "Unit 1: Our Environment", ready: true, file: "english_p5_unit1_environment.json" },
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

// 題庫URL前綴 (GitHub Raw)
const QUESTION_BASE = "https://raw.githubusercontent.com/ebuddycheung/Athena-Revision/main/questions/";

// Navigation
function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.getElementById(sectionId).classList.add('active');
}

// Subject Selection
document.querySelectorAll('.subject-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        currentSubject = btn.dataset.subject;
        const subjectName = subjects[currentSubject].name;
        document.getElementById('subject-title').textContent = 
            `📑 選擇 ${subjectName} 課文`;
        populateChapters();
        showSection('chapter-section');
    });
});

// Populate Chapters
function populateChapters() {
    const list = document.getElementById('chapter-list');
    const chapters = subjects[currentSubject]?.chapters || [];
    
    if (chapters.length === 0 || chapters.every(ch => !ch.ready)) {
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
        <button class="chapter-btn" data-chapter="${ch.id}" ${!ch.ready ? 'disabled' : ''}>
            ${ch.title}
            <span class="status ${ch.ready ? 'ready' : ''}">
                ${ch.ready ? '✓ 可用' : '⏳ 敬請期待'}
            </span>
        </button>
    `).join('');
    
    list.querySelectorAll('.chapter-btn:not([disabled])').forEach(btn => {
        btn.addEventListener('click', () => {
            currentChapter = btn.dataset.chapter;
            showSection('quiz-section');
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

// Start Quiz - 從題庫載入
async function startQuiz() {
    showSection('quiz-taking-section');
    document.getElementById('question-container').innerHTML = 
        '<div class="loading">正在載入題目...</div>';
    
    try {
        await loadQuestionsFromBank();
        displayQuestion();
    } catch (error) {
        document.getElementById('question-container').innerHTML = 
            '<div class="empty-state"><p>載入題目失敗，請稍後再試。</p></div>';
        console.error(error);
    }
}

// 從題庫載入題目
async function loadQuestionsFromBank() {
    const chapter = subjects[currentSubject].chapters.find(ch => ch.id == currentChapter);
    if (!chapter || !chapter.file) {
        throw new Error("Chapter not found");
    }
    
    const url = QUESTION_BASE + chapter.file;
    const response = await fetch(url);
    const data = await response.json();
    
    // 根據題型篩選
    let allQuestions = data.questions.filter(q => q.type === currentQuizType);
    
    // 如果該題型不夠，嘗試其他題型
    if (allQuestions.length < 3) {
        allQuestions = data.questions;
    }
    
    // 隨機排序
    allQuestions = shuffleArray(allQuestions);
    
    // 取最多10題
    currentQuestions = allQuestions.slice(0, 10);
    
    currentQuestionIndex = 0;
    userAnswers = {};
}

// Fisher-Yates 洗牌算法
function shuffleArray(array) {
    const arr = [...array];
    for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
}

// Display Question
function displayQuestion() {
    const q = currentQuestions[currentQuestionIndex];
    const container = document.getElementById('question-container');
    
    document.getElementById('progress').textContent = 
        `第 ${currentQuestionIndex + 1}/${currentQuestions.length} 題`;
    
    let html = `<p class="question-text">${q.question}</p>`;
    
    if (q.type === 'mcq' || q.type === 'truefalse') {
        html += '<div class="options">';
        q.options.forEach((opt, i) => {
            html += `
                <label class="option" data-index="${i}">
                    <input type="radio" name="answer" value="${i}">
                    ${opt}
                </label>
            `;
        });
        html += '</div>';
    } else if (q.type === 'fillblank') {
        html += `
            <input type="text" class="fill-input" 
                placeholder="請輸入答案...">
        `;
    } else if (q.type === 'shortanswer') {
        html += `
            <textarea class="fill-input short-answer" 
                placeholder="請輸入你的答案..."></textarea>
        `;
    }
    
    container.innerHTML = html;
    
    // 更新導航按鈕
    document.getElementById('prev-btn').disabled = currentQuestionIndex === 0;
    
    if (currentQuestionIndex === currentQuestions.length - 1) {
        document.getElementById('next-btn').style.display = 'none';
        document.getElementById('submit-btn').style.display = 'inline-block';
    } else {
        document.getElementById('next-btn').style.display = 'inline-block';
        document.getElementById('submit-btn').style.display = 'none';
    }
    
    // 事件監聽
    container.querySelectorAll('input[name="answer"]').forEach(input => {
        input.addEventListener('change', (e) => {
            const label = e.target.parentElement;
            container.querySelectorAll('.option').forEach(l => l.classList.remove('selected'));
            label.classList.add('selected');
            userAnswers[q.id] = e.target.value;
        });
    });
    
    const textInput = container.querySelector('.fill-input');
    if (textInput) {
        textInput.addEventListener('input', (e) => {
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
    let correct = 0;
    let resultsHTML = '';
    
    currentQuestions.forEach((q, i) => {
        let userAns = userAnswers[q.id];
        let isCorrect = false;
        
        if (q.type === 'mcq' || q.type === 'truefalse') {
            // 用戶選擇的選項文字 vs 正確答案文字
            const selectedOption = q.options[userAns];
            isCorrect = selectedOption === q.answer;
            if (isCorrect) correct++;
        } else if (q.type === 'fillblank') {
            isCorrect = userAns?.toLowerCase().trim() === q.answer.toLowerCase().trim();
            if (isCorrect) correct++;
        } else if (q.type === 'shortanswer') {
            // 短答題不計分，只顯示參考答案
            isCorrect = null;
        }
        
        // 加入答題覆習
        let statusIcon = '';
        let statusClass = '';
        if (isCorrect === true) {
            statusIcon = '✅';
            statusClass = 'correct';
        } else if (isCorrect === false) {
            statusIcon = '❌';
            statusClass = 'incorrect';
        } else {
            statusIcon = '📝';
            statusClass = 'review';
        }
        
        // 取得用戶答案的文字
        let userAnswerText = '';
        let correctAnswerText = '';
        
        if (q.type === 'mcq' || q.type === 'truefalse') {
            userAnswerText = q.options[userAns] || '未答';
            correctAnswerText = q.options[q.answer] || q.answer;
        } else {
            userAnswerText = userAns || '未答';
            correctAnswerText = q.answer;
        }
        
        resultsHTML += `
            <div class="review-item ${statusClass}">
                <div class="review-header">
                    <span>${statusIcon} 第 ${i + 1} 題</span>
                </div>
                <p class="review-question">${q.question}</p>
                <p>你的答案：${userAnswerText}</p>
                <p>正確答案：${correctAnswerText}</p>
                <p class="explanation">💡 ${q.explanation}</p>
                ${q.type === 'shortanswer' && q.sampleAnswer ? `
                    <p class="sample-answer">📋 參考答案：${q.sampleAnswer}</p>
                ` : ''}
            </div>
        `;
    });
    
    document.getElementById('score').textContent = correct;
    document.getElementById('total').textContent = currentQuestions.length;
    
    const percentage = (correct / currentQuestions.length) * 100;
    let message = '';
    if (percentage >= 90) message = '🌟 太棒了！完全掌握！';
    else if (percentage >= 70) message = '👍 做得好！繼續加油！';
    else if (percentage >= 50) message = '📚 還有進步空間，多溫習！';
    else message = '💪 加油！温習後再試！';
    
    document.getElementById('score-message').textContent = message;
    document.getElementById('review-section').innerHTML = resultsHTML;
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

// Initialize
console.log('Athena 温習助手 loaded! 👺');
console.log('題庫來源: ' + QUESTION_BASE);
