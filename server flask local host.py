# -*- coding: utf-8 -*-
"""
OXTEAM HUB — всё в одном файле
Запуск: python app.py
Открыть: http://localhost:5000
"""

from flask import Flask, render_template_string, jsonify, request
import os
import subprocess
import sys
import tempfile

app = Flask(__name__)

# ============================================================
#                    HTML + CSS + JS
# ============================================================
INDEX_HTML = r"""
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OXTEAM HUB</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Arial, sans-serif; }
body {
  background: radial-gradient(circle at 50% 0%, #0a001f 0%, #000 100%);
  color: #e0e0e0;
  min-height: 100vh;
  padding-bottom: 40px;
}
header {
  text-align: center;
  padding: 40px 20px 20px;
  border-bottom: 2px solid #00ff88;
  box-shadow: 0 0 30px #00ff8855;
  margin-bottom: 20px;
}
header h1 {
  font-size: 3em;
  background: linear-gradient(90deg, #00ff88, #ff00ff, #00aaff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: 4px;
  filter: drop-shadow(0 0 20px #00ff88);
}
header p { color: #888; margin-top: 10px; letter-spacing: 2px; }

.menu { display: flex; justify-content: center; gap: 25px; flex-wrap: wrap; padding: 30px 20px; }
.menu-card {
  background: linear-gradient(145deg, #111, #1a1a2e);
  border: 2px solid #00ff88;
  border-radius: 16px;
  width: 240px; padding: 25px 20px;
  text-align: center; cursor: pointer;
  transition: 0.3s;
  box-shadow: 0 0 15px #00ff8833;
}
.menu-card:hover {
  transform: translateY(-8px) scale(1.03);
  box-shadow: 0 0 30px #00ff88, 0 0 60px #ff00ff55;
  border-color: #ff00ff;
}
.menu-card .icon { font-size: 3.5em; margin-bottom: 10px; }
.menu-card h3 { color: #00ff88; font-size: 1.2em; letter-spacing: 2px; margin-bottom: 8px; }
.menu-card p { color: #aaa; font-size: 0.85em; }

.section { display: none; padding: 20px 30px; max-width: 1200px; margin: 0 auto; }
.section.active { display: block; animation: fadeIn 0.4s; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: none; } }
.section h2 {
  text-align: center; color: #00ff88; font-size: 2em;
  margin-bottom: 25px; letter-spacing: 3px;
  text-shadow: 0 0 20px #00ff88;
}
.back-btn {
  background: #ff00ff22; border: 1px solid #ff00ff;
  color: #ff00ff; padding: 8px 20px; border-radius: 8px;
  cursor: pointer; margin-bottom: 20px; transition: 0.3s;
}
.back-btn:hover { background: #ff00ff; color: #000; }

.gen-form {
  background: #111; border: 2px solid #00aaff;
  border-radius: 16px; padding: 25px; margin-bottom: 30px;
}
.gen-form h3 { color: #00aaff; margin-bottom: 20px; }
.gen-form label { display: block; margin-bottom: 15px; color: #ccc; }
.gen-form input[type=text], .gen-form select {
  width: 100%; padding: 10px; margin-top: 5px;
  background: #0a0a0a; border: 1px solid #333;
  border-radius: 6px; color: #00ff88; font-size: 1em;
}
.gen-form input[type=color] {
  width: 60px; height: 40px; border: none;
  cursor: pointer; background: transparent;
}
.templates {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px; margin-top: 20px;
}
.template-card {
  background: #111; border: 1px solid #00aaff;
  border-radius: 12px; padding: 20px; transition: 0.3s;
}
.template-card:hover { box-shadow: 0 0 25px #00aaff; }
.template-card h4 { color: #00aaff; margin-bottom: 10px; }
.template-card p { color: #888; font-size: 0.9em; margin-bottom: 15px; }

.btn {
  background: #00ff88; color: #000; border: none;
  padding: 10px 20px; border-radius: 8px; cursor: pointer;
  font-weight: bold; letter-spacing: 1px; transition: 0.3s;
}
.btn:hover { background: #00cc66; box-shadow: 0 0 20px #00ff88; }
.btn-magenta { background: #ff00ff; color: #fff; }
.btn-magenta:hover { background: #cc00cc; box-shadow: 0 0 20px #ff00ff; }

.music-panel {
  background: #111; border: 2px solid #ff00ff;
  border-radius: 16px; padding: 25px; margin-bottom: 20px;
  text-align: center; box-shadow: 0 0 25px #ff00ff33;
}
.music-panel h3 { color: #ff00ff; margin-bottom: 15px; }
.music-params { margin: 15px 0; }
.beat-display { display: flex; justify-content: center; gap: 12px; margin-top: 20px; }
.beat-dot { width: 18px; height: 18px; border-radius: 50%; background: #222; transition: 0.1s; }
.beat-dot.active { background: #ff00ff; box-shadow: 0 0 20px #ff00ff; transform: scale(1.3); }

.games-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 20px; }
.game-card {
  background: linear-gradient(145deg, #111, #1a001a);
  border: 2px solid #00aaff; border-radius: 12px;
  padding: 25px; text-align: center; cursor: pointer; transition: 0.3s;
}
.game-card:hover { border-color: #00ff88; box-shadow: 0 0 25px #00ff88; transform: scale(1.05); }
.game-card .icon { font-size: 3em; }
.game-card h4 { color: #00aaff; margin-top: 10px; letter-spacing: 2px; }

.game-area { display: none; text-align: center; margin-top: 20px; }
.game-area.active { display: block; }
canvas {
  background: #000; border: 2px solid #00ff88;
  box-shadow: 0 0 25px #00ff8855; border-radius: 8px; max-width: 100%;
}
.game-info { color: #00ff88; font-size: 1.1em; margin: 12px 0; letter-spacing: 2px; }

.python-games {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 20px; margin-top: 20px;
}
.python-game-card {
  background: #111; border: 2px solid #00aaff;
  border-radius: 12px; padding: 20px; cursor: pointer; transition: 0.3s;
}
.python-game-card:hover { box-shadow: 0 0 25px #00aaff; transform: scale(1.02); }
.python-game-card h4 { color: #00aaff; margin-bottom: 8px; }
.python-game-card p { color: #888; font-size: 0.9em; }

.python-console {
  background: #0a0a0a; border: 2px solid #00ff88;
  border-radius: 12px; padding: 20px; margin-top: 20px;
}
.python-console h3 { color: #00ff88; margin-bottom: 15px; }
#pyOutput {
  background: #000; color: #00ff88; padding: 15px;
  border-radius: 8px; min-height: 200px; max-height: 400px;
  overflow-y: auto; font-family: 'Consolas', monospace;
  font-size: 0.95em; white-space: pre-wrap;
  border: 1px solid #00ff8844;
}
.py-input-row { display: flex; gap: 10px; margin-top: 15px; }
.py-input-row input {
  flex: 1; padding: 10px; background: #0a0a0a;
  border: 1px solid #00ff88; border-radius: 6px;
  color: #00ff88; font-family: 'Consolas', monospace;
}
footer {
  text-align: center; padding: 25px; color: #444;
  border-top: 1px solid #222; margin-top: 40px;
}
@media (max-width: 600px) {
  header h1 { font-size: 1.8em; }
  .menu-card { width: 100%; }
  canvas { width: 100%; height: auto; }
}
</style>
</head>
<body>

<header>
  <h1>OXTEAM HUB</h1>
  <p>ГЕНЕРАТОРЫ · МУЗЫКА · ИГРЫ · PYTHON</p>
</header>

<div class="menu" id="mainMenu">
  <div class="menu-card" onclick="showSection('sectionSites')">
    <div class="icon">🌐</div><h3>ГЕНЕРАТОР САЙТОВ</h3><p>6 шаблонов + настройка</p>
  </div>
  <div class="menu-card" onclick="showSection('sectionMusic')">
    <div class="icon">🎵</div><h3>MUSIC / FONK</h3><p>Web Audio + MP3</p>
  </div>
  <div class="menu-card" onclick="showSection('sectionGames')">
    <div class="icon">🎮</div><h3>JS-ИГРЫ</h3><p>Snake · Tetris · Pong</p>
  </div>
  <div class="menu-card" onclick="showSection('sectionPython')">
    <div class="icon">🐍</div><h3>PYTHON-ИГРЫ</h3><p>Угадай · Виселица · Викторина</p>
  </div>
</div>

<!-- ГЕНЕРАТОР САЙТОВ -->
<div class="section" id="sectionSites">
  <button class="back-btn" onclick="showMain()">← Назад</button>
  <h2>🌐 ГЕНЕРАТОР САЙТОВ</h2>
  <div class="gen-form">
    <h3>⚙️ Настрой свой сайт</h3>
    <label>Название: <input type="text" id="siteTitle" value="Мой Сайт"></label>
    <label>Подзаголовок: <input type="text" id="siteSub" value="Добро пожаловать"></label>
    <label>Цвет: <input type="color" id="siteColor" value="#00ff88"></label>
    <label>Шаблон:
      <select id="siteTemplate">
        <option value="portfolio">Портфолио</option>
        <option value="card">Визитка</option>
        <option value="shop">Магазин</option>
        <option value="blog">Блог</option>
        <option value="landing">Лендинг</option>
        <option value="gallery">Галерея</option>
      </select>
    </label>
    <button class="btn" onclick="generateSite()">🎨 Сгенерировать и скачать</button>
  </div>
  <h3 style="margin-top:30px;color:#00aaff;">Готовые шаблоны:</h3>
  <div class="templates" id="templatesGrid"></div>
</div>

<!-- МУЗЫКА -->
<div class="section" id="sectionMusic">
  <button class="back-btn" onclick="showMain()">← Назад</button>
  <h2>🎵 MUSIC / FONK</h2>
  <div class="music-panel">
    <h3>🎧 Генератор фонк-бита</h3>
    <p style="color:#888;">Web Audio API · синтез в реальном времени</p>
    <div class="music-params">
      BPM: <input type="range" id="bpm" min="60" max="180" value="120" oninput="updateBpm(this.value)">
      <span id="bpmValue">120</span>
    </div>
    <button class="btn btn-magenta" id="playBeatBtn" onclick="toggleBeat()">▶ ИГРАТЬ</button>
    <div class="beat-display" id="beatDisplay">
      <div class="beat-dot"></div><div class="beat-dot"></div>
      <div class="beat-dot"></div><div class="beat-dot"></div>
    </div>
  </div>
  <div class="music-panel">
    <h3>📁 Локальный плеер</h3>
    <input type="file" id="musicFile" accept="audio/*" style="display:none;" onchange="loadAudio(event)">
    <button class="btn" onclick="document.getElementById('musicFile').click()">📂 ЗАГРУЗИТЬ MP3</button>
    <audio id="audioPlayer" controls style="width:100%; margin-top:15px;"></audio>
  </div>
</div>

<!-- JS-ИГРЫ -->
<div class="section" id="sectionGames">
  <button class="back-btn" onclick="showMain()">← Назад</button>
  <h2>🎮 JS-ИГРЫ</h2>
  <div class="games-grid" id="gamesGrid">
    <div class="game-card" onclick="startGame('snake')"><div class="icon">🐍</div><h4>SNAKE</h4></div>
    <div class="game-card" onclick="startGame('tetris')"><div class="icon">🧱</div><h4>TETRIS</h4></div>
    <div class="game-card" onclick="startGame('pong')"><div class="icon">🏓</div><h4>PONG</h4></div>
  </div>
  <div class="game-area" id="gameArea">
    <button class="back-btn" onclick="stopGame()">← К списку</button>
    <div class="game-info" id="gameInfo">Готов к игре</div>
    <canvas id="gameCanvas" width="600" height="400"></canvas>
  </div>
</div>

<!-- PYTHON-ИГРЫ -->
<div class="section" id="sectionPython">
  <button class="back-btn" onclick="showMain()">← Назад</button>
  <h2>🐍 PYTHON-ИГРЫ</h2>
  <p style="text-align:center; color:#888;">Работает через Flask backend (subprocess)</p>
  <div class="python-games" id="pythonGames"></div>
  <div class="python-console" id="pythonConsole" style="display:none;">
    <button class="back-btn" onclick="closePython()">← Назад</button>
    <h3 id="pyGameTitle"></h3>
    <pre id="pyOutput">Ожидание запуска...</pre>
    <div class="py-input-row">
      <input type="text" id="pyInput" placeholder="Введи ответ..." onkeypress="if(event.key==='Enter')sendPythonInput()">
      <button class="btn" onclick="sendPythonInput()">Отправить</button>
    </div>
  </div>
</div>

<footer>OXTEAM HUB © 2025 · <span id="clock"></span></footer>

<script>
// ============ НАВИГАЦИЯ ============
function showSection(id) {
  document.getElementById('mainMenu').style.display = 'none';
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  window.scrollTo(0, 0);
  if (id === 'sectionPython') loadPythonGames();
}
function showMain() {
  stopGame();
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.getElementById('mainMenu').style.display = 'flex';
}
setInterval(() => {
  document.getElementById('clock').textContent = new Date().toLocaleTimeString('ru-RU');
}, 1000);

// ============ ГЕНЕРАТОР САЙТОВ ============
const TEMPLATES = {
  portfolio: (t, s, c) => `<!DOCTYPE html><html><head><meta charset="UTF-8"><title>${t}</title>
<style>body{margin:0;font-family:Arial;background:#0a0a0a;color:#eee;padding:60px}
h1{font-size:3em;color:${c}}h2{color:${c};margin-top:40px}
.card{background:#111;padding:20px;border-radius:10px;margin:15px 0;border-left:4px solid ${c}}</style></head>
<body><h1>${t}</h1><p>${s}</p><h2>Проекты</h2>
<div class="card"><h3>Проект 1</h3><p>Описание</p></div>
<div class="card"><h3>Проект 2</h3><p>Описание</p></div></body></html>`,
  card: (t, s, c) => `<!DOCTYPE html><html><head><meta charset="UTF-8"><title>${t}</title>
<style>body{margin:0;font-family:Arial;background:linear-gradient(135deg,#001a2e,#000);color:#fff;height:100vh;display:flex;align-items:center;justify-content:center}
.box{background:#111c;padding:50px;border-radius:20px;text-align:center;border:2px solid ${c};box-shadow:0 0 40px ${c}55}
h1{margin:0;color:${c}}.sub{color:#888;margin:10px 0 30px}</style></head>
<body><div class="box"><h1>${t}</h1><div class="sub">${s}</div>
<div>📧 email@example.com</div><div>📱 +7 999 123-45-67</div></div></body></html>`,
  shop: (t, s, c) => `<!DOCTYPE html><html><head><meta charset="UTF-8"><title>${t}</title>
<style>body{margin:0;font-family:Arial;background:#0a0a0a;color:#eee;padding:40px}
h1{text-align:center;color:${c}}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px;margin-top:40px}
.item{background:#111;padding:20px;border-radius:12px;border:1px solid ${c};text-align:center}
.price{color:${c};font-size:1.5em;margin:10px 0}
button{background:${c};border:none;padding:10px 20px;border-radius:6px;cursor:pointer;font-weight:bold}</style></head>
<body><h1>🛒 ${t}</h1><p style="text-align:center">${s}</p>
<div class="grid"><div class="item"><h3>Товар 1</h3><div class="price">999 ₽</div><button>Купить</button></div>
<div class="item"><h3>Товар 2</h3><div class="price">1999 ₽</div><button>Купить</button></div>
<div class="item"><h3>Товар 3</h3><div class="price">499 ₽</div><button>Купить</button></div></div></body></html>`,
  blog: (t, s, c) => `<!DOCTYPE html><html><head><meta charset="UTF-8"><title>${t}</title>
<style>body{margin:0;font-family:Georgia;background:#0f0f0f;color:#ddd;padding:40px;max-width:800px;margin:auto}
h1{color:${c};text-align:center}.post{background:#181818;padding:25px;border-radius:12px;margin:25px 0;border-left:4px solid ${c}}</style></head>
<body><h1>${t}</h1><p style="text-align:center;color:#888">${s}</p>
<div class="post"><h2>Первый пост</h2><p>Текст поста...</p></div>
<div class="post"><h2>Второй пост</h2><p>Текст поста...</p></div></body></html>`,
  landing: (t, s, c) => `<!DOCTYPE html><html><head><meta charset="UTF-8"><title>${t}</title>
<style>body{margin:0;font-family:Arial;background:#000;color:#fff;text-align:center}
.hero{padding:120px 20px;background:linear-gradient(135deg,${c}22,#000)}
.hero h1{font-size:4em;color:${c};margin:0 0 20px}.hero p{font-size:1.3em;color:#aaa}
.btn{background:${c};color:#000;padding:15px 40px;border-radius:8px;border:none;font-size:1.1em;font-weight:bold;margin-top:30px;cursor:pointer}
.features{display:flex;justify-content:center;gap:30px;padding:60px 20px;flex-wrap:wrap}
.feat{background:#111;padding:30px;border-radius:12px;width:250px;border-top:4px solid ${c}}</style></head>
<body><div class="hero"><h1>${t}</h1><p>${s}</p><button class="btn">Начать</button></div>
<div class="features"><div class="feat"><h3>⚡ Быстро</h3><p>Скорость</p></div>
<div class="feat"><h3>🔒 Безопасно</h3><p>Защита</p></div>
<div class="feat"><h3>💎 Красиво</h3><p>Дизайн</p></div></div></body></html>`,
  gallery: (t, s, c) => `<!DOCTYPE html><html><head><meta charset="UTF-8"><title>${t}</title>
<style>body{margin:0;font-family:Arial;background:#0a0a0a;color:#eee;padding:40px}
h1{text-align:center;color:${c}}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:15px;margin-top:30px}
.ph{aspect-ratio:1;background:linear-gradient(135deg,${c}44,#111);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:2em;border:1px solid ${c}}</style></head>
<body><h1>${t}</h1><p style="text-align:center;color:#888">${s}</p>
<div class="grid">${Array.from({length:9}).map((_, i) => `<div class="ph">🖼️ ${i+1}</div>`).join('')}</div></body></html>`,
};

function generateSite() {
  const t = document.getElementById('siteTitle').value || 'Мой Сайт';
  const s = document.getElementById('siteSub').value || 'Добро пожаловать';
  const c = document.getElementById('siteColor').value;
  const tmpl = document.getElementById('siteTemplate').value;
  const html = TEMPLATES[tmpl](t, s, c);
  const blob = new Blob([html], { type: 'text/html' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `${tmpl}_${t.replace(/\s+/g, '_')}.html`;
  a.click();
}

window.addEventListener('DOMContentLoaded', () => {
  const grid = document.getElementById('templatesGrid');
  const names = { portfolio:'Портфолио', card:'Визитка', shop:'Магазин',
                  blog:'Блог', landing:'Лендинг', gallery:'Галерея' };
  Object.keys(names).forEach(key => {
    const div = document.createElement('div');
    div.className = 'template-card';
    div.innerHTML = `<h4>${names[key]}</h4><p>Готовый шаблон</p>
      <button class="btn" onclick="quickDownload('${key}')">Скачать</button>`;
    grid.appendChild(div);
  });
});

function quickDownload(key) {
  document.getElementById('siteTemplate').value = key;
  generateSite();
}

// ============ МУЗЫКА ============
let audioCtx = null, beatInterval = null, beatStep = 0, beatPlaying = false, currentBpm = 120;

function updateBpm(v) {
  currentBpm = parseInt(v);
  document.getElementById('bpmValue').textContent = v;
  if (beatPlaying) {
    clearInterval(beatInterval);
    beatInterval = setInterval(playStep, 60000 / currentBpm / 4);
  }
}
function toggleBeat() {
  if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  if (beatPlaying) {
    clearInterval(beatInterval); beatPlaying = false;
    document.getElementById('playBeatBtn').textContent = '▶ ИГРАТЬ';
    document.querySelectorAll('.beat-dot').forEach(d => d.classList.remove('active'));
  } else {
    beatPlaying = true;
    document.getElementById('playBeatBtn').textContent = '⏹ СТОП';
    beatStep = 0;
    beatInterval = setInterval(playStep, 60000 / currentBpm / 4);
  }
}
function playStep() {
  const dots = document.querySelectorAll('.beat-dot');
  dots.forEach(d => d.classList.remove('active'));
  dots[beatStep % 4].classList.add('active');
  if (beatStep % 4 === 0 || beatStep % 4 === 2) playKick();
  if (beatStep % 4 === 1 || beatStep % 4 === 3) playSnare();
  playHat();
  beatStep++;
}
function playKick() {
  const osc = audioCtx.createOscillator(), gain = audioCtx.createGain();
  osc.frequency.setValueAtTime(150, audioCtx.currentTime);
  osc.frequency.exponentialRampToValueAtTime(40, audioCtx.currentTime + 0.1);
  gain.gain.setValueAtTime(0.8, audioCtx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.3);
  osc.connect(gain).connect(audioCtx.destination);
  osc.start(); osc.stop(audioCtx.currentTime + 0.3);
}
function playSnare() {
  const buf = audioCtx.createBuffer(1, audioCtx.sampleRate * 0.2, audioCtx.sampleRate);
  const d = buf.getChannelData(0);
  for (let i = 0; i < d.length; i++) d[i] = (Math.random() * 2 - 1) * (1 - i / d.length);
  const src = audioCtx.createBufferSource(); src.buffer = buf;
  const g = audioCtx.createGain(); g.gain.value = 0.4;
  src.connect(g).connect(audioCtx.destination); src.start();
}
function playHat() {
  const buf = audioCtx.createBuffer(1, audioCtx.sampleRate * 0.05, audioCtx.sampleRate);
  const d = buf.getChannelData(0);
  for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
  const src = audioCtx.createBufferSource(); src.buffer = buf;
  const g = audioCtx.createGain(); g.gain.value = 0.15;
  const f = audioCtx.createBiquadFilter(); f.type = 'highpass'; f.frequency.value = 7000;
  src.connect(f).connect(g).connect(audioCtx.destination); src.start();
}
function loadAudio(e) {
  const f = e.target.files[0];
  if (f) document.getElementById('audioPlayer').src = URL.createObjectURL(f);
}

// ============ JS-ИГРЫ ============
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
let currentGame = null, gameLoop = null;

function startGame(name) {
  document.getElementById('gamesGrid').style.display = 'none';
  document.getElementById('gameArea').classList.add('active');
  currentGame = name;
  if (name === 'snake') startSnake();
  else if (name === 'pong') startPong();
  else if (name === 'tetris') startSimpleTetris();
}
function stopGame() {
  if (gameLoop) cancelAnimationFrame(gameLoop);
  gameLoop = null; currentGame = null;
  document.getElementById('gamesGrid').style.display = 'grid';
  document.getElementById('gameArea').classList.remove('active');
}

// SNAKE
let snake, snakeDir, snakeFood, snakeScore;
document.addEventListener('keydown', e => {
  if (currentGame !== 'snake') return;
  if (e.key === 'ArrowUp' && snakeDir.y === 0) snakeDir = {x:0, y:-1};
  if (e.key === 'ArrowDown' && snakeDir.y === 0) snakeDir = {x:0, y:1};
  if (e.key === 'ArrowLeft' && snakeDir.x === 0) snakeDir = {x:-1, y:0};
  if (e.key === 'ArrowRight' && snakeDir.x === 0) snakeDir = {x:1, y:0};
});
function startSnake() {
  snake = [{x:10, y:10}]; snakeDir = {x:1, y:0}; snakeScore = 0;
  spawnFood();
  document.getElementById('gameInfo').textContent = 'Счёт: 0';
  let last = 0;
  function loop(t) {
    if (t - last > 120) { updateSnake(); drawSnake(); last = t; }
    gameLoop = requestAnimationFrame(loop);
  }
  gameLoop = requestAnimationFrame(loop);
}
function spawnFood() {
  snakeFood = { x: Math.floor(Math.random()*30), y: Math.floor(Math.random()*20) };
}
function updateSnake() {
  const h = { x: snake[0].x + snakeDir.x, y: snake[0].y + snakeDir.y };
  if (h.x < 0 || h.x >= 30 || h.y < 0 || h.y >= 20 || snake.some(s => s.x === h.x && s.y === h.y)) return gameOver();
  snake.unshift(h);
  if (h.x === snakeFood.x && h.y === snakeFood.y) {
    snakeScore += 10;
    document.getElementById('gameInfo').textContent = 'Счёт: ' + snakeScore;
    spawnFood();
  } else snake.pop();
}
function drawSnake() {
  ctx.fillStyle = '#000'; ctx.fillRect(0, 0, 600, 400);
  ctx.fillStyle = '#ff00ff'; ctx.fillRect(snakeFood.x*20, snakeFood.y*20, 18, 18);
  snake.forEach((s, i) => {
    ctx.fillStyle = i === 0 ? '#00ff88' : '#00aaff';
    ctx.fillRect(s.x*20, s.y*20, 18, 18);
  });
}
function gameOver() {
  cancelAnimationFrame(gameLoop);
  ctx.fillStyle = '#000a'; ctx.fillRect(0, 0, 600, 400);
  ctx.fillStyle = '#ff0055'; ctx.font = '40px Arial'; ctx.textAlign = 'center';
  ctx.fillText('GAME OVER', 300, 200);
  ctx.font = '20px Arial'; ctx.fillStyle = '#fff';
  ctx.fillText('Счёт: ' + snakeScore, 300, 240);
  document.getElementById('gameInfo').textContent = 'Игра окончена.';
}

// PONG
let pongBall, pongPaddle, pongAI, pongScore;
function startPong() {
  pongBall = { x: 300, y: 200, dx: 4, dy: 3 };
  pongPaddle = { x: 20, y: 160 };
  pongAI = { x: 570, y: 160 };
  pongScore = 0;
  document.getElementById('gameInfo').textContent = 'Счёт: 0';
  canvas.onmousemove = e => {
    const rect = canvas.getBoundingClientRect();
    pongPaddle.y = e.clientY - rect.top - 40;
  };
  function loop() {
    pongBall.x += pongBall.dx; pongBall.y += pongBall.dy;
    if (pongBall.y < 0 || pongBall.y > 400) pongBall.dy *= -1;
    if (pongBall.x < 40 && pongBall.y > pongPaddle.y && pongBall.y < pongPaddle.y + 80) {
      pongBall.dx = Math.abs(pongBall.dx); pongScore++;
      document.getElementById('gameInfo').textContent = 'Счёт: ' + pongScore;
    }
    if (pongBall.x > 560 && pongBall.y > pongAI.y && pongBall.y < pongAI.y + 80) pongBall.dx = -Math.abs(pongBall.dx);
    if (pongBall.x < 0 || pongBall.x > 600) {
      pongBall = { x: 300, y: 200, dx: 4, dy: 3 };
    }
    // AI следит за мячом
    const targetY = pongBall.y - 40;
    pongAI.y += (targetY - pongAI.y) * 0.05;

    ctx.fillStyle = '#000'; ctx.fillRect(0, 0, 600, 400);
    ctx.setLineDash([10, 10]); ctx.strokeStyle = '#00ff88';
    ctx.beginPath(); ctx.moveTo(300, 0); ctx.lineTo(300, 400); ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = '#00ff88'; ctx.fillRect(pongPaddle.x, pongPaddle.y, 10, 80);
    ctx.fillStyle = '#ff00ff'; ctx.fillRect(pongAI.x, pongAI.y, 10, 80);
    ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(pongBall.x, pongBall.y, 8, 0, 7); ctx.fill();

    gameLoop = requestAnimationFrame(loop);
  }
  gameLoop = requestAnimationFrame(loop);
}

// TETRIS (упрощённый — падающий блок)
let simpleBlocks, simpleSpeed;
function startSimpleTetris() {
  simpleBlocks = [];
  simpleSpeed = 1;
  let counter = 0;
  document.getElementById('gameInfo').textContent = 'Лови блоки!';
  function loop() {
    counter++;
    if (counter % 30 === 0) {
      simpleBlocks.push({ x: Math.floor(Math.random()*9)*60, y: 0, w: 60, h: 60 });
    }
    simpleBlocks.forEach(b => b.y += simpleSpeed);
    simpleBlocks = simpleBlocks.filter(b => b.y < 400);
    ctx.fillStyle = '#000'; ctx.fillRect(0, 0, 600, 400);
    simpleBlocks.forEach(b => {
      ctx.fillStyle = '#00aaff';
      ctx.fillRect(b.x, b.y, b.w - 2, b.h - 2);
    });
    gameLoop = requestAnimationFrame(loop);
  }
  gameLoop = requestAnimationFrame(loop);
}

// ============ PYTHON-ИГРЫ ============
let currentPyGame = null;
async function loadPythonGames() {
  const grid = document.getElementById('pythonGames');
  if (grid.children.length) return;
  const res = await fetch('/api/python_games');
  const games = await res.json();
  Object.keys(games).forEach(key => {
    const g = games[key];
    const div = document.createElement('div');
    div.className = 'python-game-card';
    div.innerHTML = `<h4>${g.name}</h4><p>${g.desc}</p>
      <button class="btn" style="margin-top:10px" onclick="openPython('${key}', '${g.name}')">▶ Запустить</button>`;
    grid.appendChild(div);
  });
}
function openPython(key, name) {
  currentPyGame = key;
  document.getElementById('pythonGames').style.display = 'none';
  document.getElementById('pythonConsole').style.display = 'block';
  document.getElementById('pyGameTitle').textContent = '🐍 ' + name;
  document.getElementById('pyOutput').textContent = 'Нажми "Отправить" с пустым полем, чтобы начать...';
}
function closePython() {
  currentPyGame = null;
  document.getElementById('pythonGames').style.display = 'grid';
  document.getElementById('pythonConsole').style.display = 'none';
}
async function sendPythonInput() {
  if (!currentPyGame) return;
  const inp = document.getElementById('pyInput');
  const val = inp.value;
  inp.value = '';
  const out = document.getElementById('pyOutput');
  out.textContent += '\n> ' + val;
  const res = await fetch('/api/run_python', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ game: currentPyGame, input: val + '\n' })
  });
  const data = await res.json();
  if (data.output) out.textContent += '\n' + data.output;
  if (data.error) out.textContent += '\n[ОШИБКА] ' + data.error;
  out.scrollTop = out.scrollHeight;
}
</script>
</body>
</html>
"""

# ============================================================
#                    PYTHON-ИГРЫ (встроены)
# ============================================================
PYTHON_GAMES_CODE = {
    "guess": r"""
import random, sys
n = random.randint(1, 100)
attempts = 0
print("Я загадал число от 1 до 100. Угадай!")
for line in sys.stdin:
    try:
        g = int(line.strip())
        attempts += 1
        if g < n: print(f"Больше! (попытка {attempts})")
        elif g > n: print(f"Меньше! (попытка {attempts})")
        else:
            print(f"🎉 Угадал! Число {n}, попыток: {attempts}")
            break
    except: print("Введи число")
""",
    "hangman": r"""
import sys
word = "oxteam"
guessed = set()
tries = 6
print(f"Виселица! Слово из {len(word)} букв. Попыток: {tries}")
for line in sys.stdin:
    if not line.strip(): continue
    letter = line.strip().lower()[0]
    if letter in guessed:
        print("Уже было")
    elif letter in word:
        guessed.add(letter)
        print("✅ Есть!")
    else:
        tries -= 1
        print(f"❌ Нет. Осталось попыток: {tries}")
        if tries == 0:
            print(f"Проиграл! Слово: {word}"); break
    display = " ".join(c if c in guessed else "_" for c in word)
    print(display)
    if all(c in guessed for c in word):
        print("🎉 Победа!"); break
""",
    "quiz": r"""
import sys
qs = [
    ("Столица России?", "москва"),
    ("2+2*2 = ?", "6"),
    ("Кто создал Python?", "гуидо"),
    ("Год начала Второй мировой?", "1939"),
    ("Сколько планет в Солнечной системе?", "8"),
]
score = 0
print(f"Викторина! {len(qs)} вопросов.")
i = 0
for line in sys.stdin:
    if i >= len(qs): break
    ans = line.strip().lower()
    if not ans: continue
    q, correct = qs[i]
    if correct in ans:
        print("✅ Правильно!"); score += 1
    else:
        print(f"❌ Неверно. Ответ: {correct}")
    i += 1
    if i < len(qs):
        print(qs[i][0])
    else:
        print(f"🏆 Итог: {score}/{len(qs)}")
        break
print(qs[0][0])
""",
}


# ============================================================
#                       FLASK ROUTES
# ============================================================
@app.route("/")
def index():
    return render_template_string(INDEX_HTML)


PYTHON_GAMES_META = {
    "guess": {"name": "Угадай число", "desc": "Компьютер загадал 1–100. Угадай за меньше попыток."},
    "hangman": {"name": "Виселица", "desc": "Угадай слово по буквам. 6 попыток."},
    "quiz": {"name": "Викторина", "desc": "5 вопросов на эрудицию."},
}


@app.route("/api/python_games")
def api_python_games():
    return jsonify(PYTHON_GAMES_META)


@app.route("/api/run_python", methods=["POST"])
def api_run_python():
    data = request.get_json()
    game = data.get("game")
    user_input = data.get("input", "")

    if game not in PYTHON_GAMES_CODE:
        return jsonify({"error": "Игра не найдена"})

    # Записываем код во временный файл
    tmp = os.path.join(tempfile.gettempdir(), f"oxteam_{game}.py")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(PYTHON_GAMES_CODE[game])

    try:
        res = subprocess.run(
            [sys.executable, tmp],
            input=user_input,
            capture_output=True,
            text=True,
            timeout=5,
            encoding="utf-8",
        )
        return jsonify({"output": res.stdout, "error": res.stderr})
    except subprocess.TimeoutExpired:
        return jsonify({"output": "", "error": "Превышено время (5 сек)"})
    except Exception as e:
        return jsonify({"output": "", "error": str(e)})


# ============================================================
#                        ЗАПУСК
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("  OXTEAM HUB запущен!")
    print("  Открой: http://localhost:5000")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=False)