<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Hızlı İşlem</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@700&display=swap');
    body {
      font-family: 'Roboto', sans-serif;
      background: #121212;
      color: #fff;
      text-align: center;
      margin: 0;
      padding: 0;
    }
    h1 {
      background: #007BFF;
      margin: 0;
      padding: 20px;
      font-size: 32px;
      border-radius: 5px;
    }
    #settings, #game, #scoreboard {
      margin: 20px auto;
      padding: 20px;
      background: #1e1e1e;
      border-radius: 10px;
      max-width: 400px;
      box-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
    }
    input, select, button {
      margin: 10px 0;
      padding: 10px;
      font-size: 16px;
      border-radius: 5px;
      border: none;
    }
    input[type="text"], input[type="number"] {
      width: 80%;
      text-align: center;
      background: #333;
      color: #fff;
      border: 2px solid #007BFF;
    }
    button {
      background: #007BFF;
      color: #fff;
      cursor: pointer;
      transition: 0.3s;
    }
    button:hover {
      background: #0056b3;
    }
    #questionDisplay {
      font-size: 28px;
      color: #66B2FF;
      margin: 20px 0;
    }
    #timer {
      font-size: 20px;
      color: #ff3d00;
    }
    #highScores li {
      background: #66B2FF;
      color: #000;
      margin: 5px 0;
      padding: 10px;
      border-radius: 5px;
      list-style: none;
    }
  </style>
</head>
<body>

<h1>Hızlı İşlem</h1>

<div id="settings">
  <p>İsmin:</p>
  <input type="text" id="nameInput" placeholder="İsim gir">
  <p>Zorluk:</p>
  <select id="difficulty">
    <option value="easy">Kolay</option>
    <option value="medium">Orta</option>
    <option value="hard">Zor</option>
  </select>
  <p>İşlem Türü:</p>
  <select id="operation">
    <option value="multiply">Çarpma</option>
    <option value="add">Toplama</option>
    <option value="subtract">Çıkarma</option>
    <option value="random">Karışık</option>
  </select>
  <button onclick="startGame()">Başla</button>
</div>

<div id="game" style="display:none;">
  <p id="timer">Süre: 60</p>
  <p id="questionDisplay"></p>
  <input type="number" id="inputField" placeholder="Cevabı yaz">
  <p>Skor: <span id="score">0</span></p>
</div>

<div id="scoreboard" style="display:none;">
  <h2>Skor Tablosu</h2>
  <ul id="highScores"></ul>
  <button onclick="restartGame()">Yeniden Oyna</button>
</div>

<script>
  let playerName = "";
  let score = 0;
  let timeLeft = 60;
  let correctAnswer = 0;
  let timer;
  let highScores = JSON.parse(localStorage.getItem("highScores") || "[]");

  const questionDisplay = document.getElementById("questionDisplay");
  const inputField = document.getElementById("inputField");
  const scoreDisplay = document.getElementById("score");
  const timerDisplay = document.getElementById("timer");
  const game = document.getElementById("game");
  const scoreboard = document.getElementById("scoreboard");
  const highScoresList = document.getElementById("highScores");

  function getMaxNumber(difficulty) {
    switch (difficulty) {
      case "easy": return 10;
      case "medium": return 25;
      case "hard": return 50;
    }
  }

  function generateQuestion() {
    const difficulty = document.getElementById("difficulty").value;
    const operation = document.getElementById("operation").value;

    const max = getMaxNumber(difficulty);
    let num1 = Math.floor(Math.random() * max) + 1;
    let num2 = Math.floor(Math.random() * max) + 1;

    let op = operation;
    if (operation === "random") {
      const ops = ["add", "subtract", "multiply"];
      op = ops[Math.floor(Math.random() * ops.length)];
    }

    switch (op) {
      case "add":
        correctAnswer = num1 + num2;
        questionDisplay.textContent = `${num1} + ${num2} = ?`;
        break;
      case "subtract":
        correctAnswer = num1 - num2;
        questionDisplay.textContent = `${num1} - ${num2} = ?`;
        break;
      case "multiply":
      default:
        correctAnswer = num1 * num2;
        questionDisplay.textContent = `${num1} × ${num2} = ?`;
        break;
    }
  }

  function updateScore() {
    score += 3;
    scoreDisplay.textContent = score;
  }

  function updateHighScores() {
    highScores.push({ name: playerName, score });
    highScores.sort((a, b) => b.score - a.score);
    highScores = highScores.slice(0, 10);
    localStorage.setItem("highScores", JSON.stringify(highScores));
    highScoresList.innerHTML = "";
    highScores.forEach((hs, i) => {
      const li = document.createElement("li");
      li.textContent = `${i + 1}. ${hs.name}: ${hs.score}`;
      highScoresList.appendChild(li);
    });
  }

  function startGame() {
    playerName = document.getElementById("nameInput").value.trim();
    if (!playerName) {
      alert("İsmini yaz be!");
      return;
    }
    document.getElementById("settings").style.display = "none";
    game.style.display = "block";
    score = 0;
    timeLeft = 60;
    scoreDisplay.textContent = score;
    inputField.disabled = false;
    generateQuestion();
    startTimer();
  }

  function startTimer() {
    timer = setInterval(() => {
      timeLeft--;
      timerDisplay.textContent = `Süre: ${timeLeft}`;
      if (timeLeft <= 0) {
        clearInterval(timer);
        game.style.display = "none";
        scoreboard.style.display = "block";
        updateHighScores();
      }
    }, 1000);
  }

  inputField.addEventListener("input", () => {
    if (parseInt(inputField.value) === correctAnswer) {
      updateScore();
      generateQuestion();
      inputField.value = "";
    }
  });

  function restartGame() {
    document.getElementById("settings").style.display = "block";
    scoreboard.style.display = "none";
    inputField.value = "";
  }
</script>
</body>
</html>

