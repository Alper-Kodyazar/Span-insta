# Yeni tasarımı ve işlevleri içerecek dosya yolu
final_html_path = "/mnt/data/hizli-islem-final-tasarim-guncel.html"

# Şık tasarıma uygun, animasyon ve rozetli yeni birleşik HTML kodu hazırlanacak
html_combined_with_design = """<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Hızlı İşlem</title>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;700&display=swap" rel="stylesheet"/>
  <style>
    :root {
      --bg-dark: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
      --accent: linear-gradient(135deg, #00c6ff, #0072ff);
      --input-bg: #ffffff10;
      --input-border: #ffffff30;
      --success: #00ff99;
      --warning: #ff6f61;
    }
    * {
      box-sizing: border-box;
    }
    body {
      margin: 0;
      font-family: 'Poppins', sans-serif;
      background: var(--bg-dark);
      color: #fff;
      display: flex;
      flex-direction: column;
      align-items: center;
      min-height: 100vh;
      justify-content: center;
      padding: 20px;
      transition: background 0.5s, color 0.5s;
    }
    h1 {
      font-size: 40px;
      margin-bottom: 20px;
      background: var(--accent);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .card {
      background: rgba(255, 255, 255, 0.05);
      border-radius: 20px;
      padding: 30px;
      max-width: 400px;
      width: 100%;
      backdrop-filter: blur(10px);
      box-shadow: 0 8px 32px rgba(0,0,0,0.3);
      text-align: center;
      margin: 20px 0;
    }
    input, select, button {
      width: 100%;
      padding: 12px;
      margin-top: 10px;
      border: none;
      border-radius: 10px;
      font-size: 16px;
      font-family: inherit;
    }
    input, select {
      background: var(--input-bg);
      color: #fff;
      border: 1px solid var(--input-border);
    }
    button {
      background: var(--accent);
      color: white;
      font-weight: bold;
      cursor: pointer;
      transition: transform 0.2s ease;
    }
    button:hover {
      transform: scale(1.05);
    }
    #questionDisplay {
      font-size: 28px;
      color: #66B2FF;
      margin: 20px 0;
    }
    #timer {
      font-size: 20px;
      color: var(--warning);
      margin: 10px 0;
    }
    .xp-bar {
      background: #ffffff30;
      border-radius: 10px;
      overflow: hidden;
      margin-top: 10px;
    }
    .xp-fill {
      height: 12px;
      background: var(--success);
      width: 0%;
      transition: width 0.3s;
    }
    body.correct {
      animation: correctFlash 0.3s;
    }
    body.wrong {
      animation: wrongFlash 0.3s;
    }
    @keyframes correctFlash {
      0% { background-color: #0f2027; }
      50% { background-color: #2ecc71; }
      100% { background-color: #0f2027; }
    }
    @keyframes wrongFlash {
      0% { background-color: #0f2027; }
      50% { background-color: #e74c3c; }
      100% { background-color: #0f2027; }
    }
    .badge {
      display: inline-block;
      background: gold;
      color: black;
      padding: 2px 8px;
      margin-left: 5px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <h1>Hızlı İşlem</h1>
  <div id="settings" class="card">
    <input type="text" id="nameInput" placeholder="İsmini gir">
    <select id="difficulty">
      <option value="easy">Kolay</option>
      <option value="medium">Orta</option>
      <option value="hard">Zor</option>
    </select>
    <select id="operation">
      <option value="multiply">Çarpma</option>
      <option value="add">Toplama</option>
      <option value="subtract">Çıkarma</option>
      <option value="random">Karışık</option>
    </select>
    <select id="gameMode">
      <option value="normal">Normal Mod</option>
      <option value="fast">Hızlı Mod (20sn)</option>
      <option value="bomb">Zaman Bombası</option>
    </select>
    <button id="startButton">Oyuna Başla</button>
  </div>
  <div id="game" class="card" style="display:none;">
    <p id="timer">Süre: 30</p>
    <div id="questionDisplay"></div>
    <input type="number" id="inputField" placeholder="Cevap">
    <p>Skor: <span id="score">0</span></p>
    <p>Seviye: <span id="level">1</span> | XP: <span id="xp">0</span></p>
    <div class="xp-bar"><div class="xp-fill" id="xpFill"></div></div>
  </div>
  <div id="scoreboard" class="card" style="display:none;">
    <h2>Liderlik Tablosu</h2>
    <ul id="highScores"></ul>
    <button onclick="restartGame()">Yeniden Oyna</button>
  </div>
  <script>
    let score = 0, xp = 0, level = 1, timeLeft = 30, correctAnswer = 0, timer, mode;
    const get = id => document.getElementById(id);

    function startGame() {
      const name = get("nameInput").value.trim();
      if (!name) return alert("İsim gir!");
      mode = get("gameMode").value;
      timeLeft = mode === "fast" ? 20 : 30;
      score = xp = 0; level = 1;
      get("settings").style.display = "none";
      get("game").style.display = "block";
      get("score").textContent = score;
      get("xp").textContent = xp;
      get("level").textContent = level;
      get("xpFill").style.width = "0%";
      generateQuestion();
      startTimer();
    }

    function startTimer() {
      timer = setInterval(() => {
        timeLeft--;
        get("timer").textContent = "Süre: " + timeLeft;
        if (timeLeft <= 0) {
          clearInterval(timer);
          endGame();
        }
      }, 1000);
    }

    function generateQuestion() {
      const op = get("operation").value;
      const difficulty = get("difficulty").value;
      const max = difficulty === "easy" ? 10 : difficulty === "medium" ? 25 : 50;
      const a = Math.floor(Math.random() * max) + 1;
      const b = Math.floor(Math.random() * max) + 1;
      const realOp = op === "random" ? ["add", "subtract", "multiply"][Math.floor(Math.random() * 3)] : op;

      if (realOp === "add") { correctAnswer = a + b; get("questionDisplay").textContent = `${a} + ${b} = ?`; }
      else if (realOp === "subtract") { correctAnswer = a - b; get("questionDisplay").textContent = `${a} - ${b} = ?`; }
      else { correctAnswer = a * b; get("questionDisplay").textContent = `${a} × ${b} = ?`; }
    }

    function getBadge(xp, score, level) {
      if (level >= 10) return '👑';
      if (score >= 500) return '💥';
      if (xp >= 100) return '🐣';
      return '';
    }

    function flashFeedback(type) {
      document.body.classList.add(type);
      setTimeout(() => document.body.classList.remove(type), 300);
    }

    document.getElementById("inputField").addEventListener("input", () => {
      const answer = parseInt(get("inputField").value);
      if (!isNaN(answer)) {
        if (answer === correctAnswer) {
          score += 3;
          xp += 5;
          if (xp >= 30) { xp = 0; level++; }
          get("score").textContent = score;
          get("xp").textContent = xp;
          get("level").textContent = level;
          get("xpFill").style.width = (xp / 30 * 100) + "%";
          get("inputField").value = "";
          generateQuestion();
          flashFeedback("correct");
        } else {
          if (mode === "bomb") timeLeft = Math.max(0, timeLeft - 3);
          flashFeedback("wrong");
        }
      }
    });

    function endGame() {
      get("game").style.display = "none";
      get("scoreboard").style.display = "block";
      const hs = JSON.parse(localStorage.getItem("scores") || "[]");
      hs.push({score, badge: getBadge(xp, score, level)});
      hs.sort((a, b) => b.score - a.score);
      localStorage.setItem("scores", JSON.stringify(hs.slice(0, 10)));
      get("highScores").innerHTML = hs.slice(0, 10)
        .map((s, i) => `<li>${i + 1}. ${s.score} puan ${s.badge ? `<span class='badge'>${s.badge}</span>` : ''}</li>`)
        .join("");
    }

    function restartGame() {
      get("scoreboard").style.display = "none";
      get("settings").style.display = "block";
    }

    document.getElementById("startButton").addEventListener("click", startGame);
  </script>
</body>
</html>
"""

# Dosyaya yaz
with open(final_html_path, "w", encoding="utf-8") as f:
    f.write(html_combined_with_design)

final_html_path
