// ---- Game state ----
let quizQuestions = [];   // the questions for the current run
let currentIndex = 0;
let score = 0;
let answered = false;

// ---- Element refs ----
const screens = {
  start: document.getElementById("screen-start"),
  quiz: document.getElementById("screen-quiz"),
  results: document.getElementById("screen-results"),
};

const topicList = document.getElementById("topic-list");
const btnAll = document.getElementById("btn-all");
const btnNext = document.getElementById("btn-next");
const btnRestart = document.getElementById("btn-restart");

const quizTopic = document.getElementById("quiz-topic");
const quizProgress = document.getElementById("quiz-progress");
const progressFill = document.getElementById("progress-fill");
const questionText = document.getElementById("question-text");
const optionsBox = document.getElementById("options");
const feedbackBox = document.getElementById("feedback");
const feedbackTitle = document.getElementById("feedback-title");
const feedbackExplanation = document.getElementById("feedback-explanation");
const liveScore = document.getElementById("live-score");

// ---- Helpers ----
function showScreen(name) {
  Object.values(screens).forEach((s) => s.classList.remove("active"));
  screens[name].classList.add("active");
}

function shuffle(array) {
  const a = [...array];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

// ---- Build the topic selection screen ----
function buildTopicList() {
  topicList.innerHTML = "";
  Object.keys(QUESTION_BANK).forEach((topic) => {
    const count = QUESTION_BANK[topic].length;
    const btn = document.createElement("button");
    btn.className = "topic-btn";
    btn.innerHTML = `${topic}<small>${count} question${count !== 1 ? "s" : ""}</small>`;
    btn.addEventListener("click", () => startQuiz(topic));
    topicList.appendChild(btn);
  });
}

// ---- Start a quiz ----
function startQuiz(topic) {
  if (topic === "ALL") {
    quizQuestions = [];
    Object.entries(QUESTION_BANK).forEach(([t, qs]) => {
      qs.forEach((q) => quizQuestions.push({ ...q, topic: t }));
    });
    quizTopic.textContent = "Full Challenge";
  } else {
    quizQuestions = QUESTION_BANK[topic].map((q) => ({ ...q, topic }));
    quizTopic.textContent = topic;
  }

  quizQuestions = shuffle(quizQuestions);
  currentIndex = 0;
  score = 0;
  liveScore.textContent = "0";
  showScreen("quiz");
  renderQuestion();
}

// ---- Render current question ----
function renderQuestion() {
  answered = false;
  const q = quizQuestions[currentIndex];

  quizProgress.textContent = `Question ${currentIndex + 1} of ${quizQuestions.length}`;
  progressFill.style.width = `${(currentIndex / quizQuestions.length) * 100}%`;
  questionText.textContent = q.question;

  optionsBox.innerHTML = "";
  q.options.forEach((opt, i) => {
    const btn = document.createElement("button");
    btn.className = "option";
    btn.textContent = opt;
    btn.addEventListener("click", () => selectAnswer(i));
    optionsBox.appendChild(btn);
  });

  feedbackBox.classList.add("hidden");
}

// ---- Handle an answer ----
function selectAnswer(chosen) {
  if (answered) return;
  answered = true;

  const q = quizQuestions[currentIndex];
  const optionButtons = optionsBox.querySelectorAll(".option");

  optionButtons.forEach((btn, i) => {
    btn.disabled = true;
    if (i === q.answer) btn.classList.add("correct");
    if (i === chosen && chosen !== q.answer) btn.classList.add("wrong");
  });

  const isCorrect = chosen === q.answer;
  if (isCorrect) {
    score++;
    liveScore.textContent = score;
    feedbackTitle.textContent = "✅ Correct!";
    feedbackTitle.className = "feedback-title correct";
  } else {
    feedbackTitle.textContent = "❌ Not quite.";
    feedbackTitle.className = "feedback-title wrong";
  }

  feedbackExplanation.textContent = q.explanation;
  feedbackBox.classList.remove("hidden");

  btnNext.textContent =
    currentIndex + 1 < quizQuestions.length ? "Next →" : "See Results →";
}

// ---- Next question / finish ----
function nextQuestion() {
  currentIndex++;
  if (currentIndex < quizQuestions.length) {
    renderQuestion();
  } else {
    showResults();
  }
}

// ---- Results ----
function showResults() {
  const total = quizQuestions.length;
  const pct = Math.round((score / total) * 100);

  document.getElementById("result-score").textContent = `${score} / ${total}  (${pct}%)`;

  let emoji, message;
  if (pct === 100) {
    emoji = "🏆"; message = "Perfect! You've mastered these concepts.";
  } else if (pct >= 75) {
    emoji = "🎓"; message = "Great job! You have a strong grasp of the material.";
  } else if (pct >= 50) {
    emoji = "📚"; message = "Good effort — review the explanations and try again!";
  } else {
    emoji = "💪"; message = "Keep going! Re-read the explanations and give it another shot.";
  }

  document.getElementById("result-emoji").textContent = emoji;
  document.getElementById("result-message").textContent = message;
  showScreen("results");
}

// ---- Events ----
btnAll.addEventListener("click", () => startQuiz("ALL"));
btnNext.addEventListener("click", nextQuestion);
btnRestart.addEventListener("click", () => showScreen("start"));

// ---- Init ----
buildTopicList();
showScreen("start");
