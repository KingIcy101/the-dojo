const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.MC_PORT || 7900;
const WORKSPACE = process.env.WORKSPACE || '/Users/mattbender/.openclaw/workspace';

app.use(express.static(path.join(__dirname, 'public')));
app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  next();
});

// ─── Helpers ───────────────────────────────────────────────────────────────

function readFile(relPath) {
  try {
    return fs.readFileSync(path.join(WORKSPACE, relPath), 'utf8');
  } catch { return ''; }
}

function readJSON(relPath) {
  try {
    return JSON.parse(fs.readFileSync(path.join(WORKSPACE, relPath), 'utf8'));
  } catch { return null; }
}

// ─── Parse win-log.md ──────────────────────────────────────────────────────

function parseWinLog() {
  const text = readFile('memory/win-log.md');
  const wins = [];
  const streakMatch = text.match(/Current Streak:\s*(\d+)/i);
  const streak = streakMatch ? parseInt(streakMatch[1]) : 0;

  // Group wins by date
  const sections = text.split(/^## (.*)/m).slice(1);
  const byDate = {};
  for (let i = 0; i < sections.length; i += 2) {
    const date = sections[i]?.trim();
    const body = sections[i + 1] || '';
    if (!date) continue;
    const dayWins = [...body.matchAll(/[-•]\s*✅\s*(.+?)(?:\s*—\s*(.+))?$/gm)]
      .map(m => ({ text: m[1].trim(), agent: m[2]?.trim() || 'Alo', date }));
    if (dayWins.length) byDate[date] = dayWins;
    wins.push(...dayWins);
  }

  return { wins: wins.slice(0, 25), streak, byDate };
}

// ─── Parse Todo.md ─────────────────────────────────────────────────────────

function parseTodo() {
  const text = readFile('Todo.md');
  const sections = { todo: [], inProgress: [], blocked: [], done: [] };

  const sectionMap = {
    'high priority': 'blocked',
    'in progress': 'inProgress',
    'agent work': 'todo',
    'upcoming': 'todo',
    'completed': 'done',
  };

  let currentSection = null;
  for (const line of text.split('\n')) {
    const header = line.match(/^##\s*(.*)/i);
    if (header) {
      const h = header[1].toLowerCase();
      currentSection = Object.keys(sectionMap).find(k => h.includes(k)) || null;
      continue;
    }
    if (!currentSection) continue;
    const target = sectionMap[currentSection];
    const taskMatch = line.match(/^\s*[-*]\s*\[([x! ])\]\s*\*?\*?(.+?)\*?\*?\s*(?:—(.*))?$/i);
    if (!taskMatch) continue;
    const [, status, title, note] = taskMatch;
    const task = {
      title: title.replace(/\*\*/g, '').trim(),
      note: note?.trim() || '',
      done: status === 'x',
      blocked: status === '!',
    };
    if (task.done) { sections.done.push(task); continue; }
    if (task.blocked) { sections.blocked.push(task); continue; }
    sections[target].push(task);
  }

  return sections;
}

// ─── Parse clients ─────────────────────────────────────────────────────────

function parseClients() {
  const data = readJSON('halo-marketing/clients/client-tracker.json');
  if (!data) return { active: [], pipeline: [] };
  return {
    active: data.clients || [],
    pipeline: data.pipeline || [],
    lastUpdated: data.lastUpdated,
  };
}

// ─── Parse agent stats ─────────────────────────────────────────────────────

function getAgents() {
  return [
    { id: 'alo',    name: 'Alo',    role: 'Orchestrator',           emoji: '🌟', status: 'online', color: '#6c63ff' },
    { id: 'scout',  name: 'Scout',  role: 'Sales Intelligence',     emoji: '🔍', status: 'online', color: '#3b9eff' },
    { id: 'rex',    name: 'Rex',    role: 'Outreach',               emoji: '🎯', status: 'online', color: '#ff5e6c' },
    { id: 'ember',  name: 'Ember',  role: 'Client Success',         emoji: '💛', status: 'online', color: '#f5b731' },
    { id: 'volt',   name: 'Volt',   role: 'Paid Ads',               emoji: '⚡', status: 'online', color: '#00d48a' },
    { id: 'prism',  name: 'Prism',  role: 'Content & Brand',        emoji: '🎨', status: 'online', color: '#ff64b4' },
    { id: 'kargo',  name: 'Kargo',  role: 'Amazon / Walmart',       emoji: '📦', status: 'online', color: '#00c8b4' },
    { id: 'atlas',  name: 'Atlas',  role: 'Chief of Staff',         emoji: '🧭', status: 'online', color: '#ff8c3c' },
    { id: 'titan',  name: 'Titan',  role: 'Entrepreneur Mentor',    emoji: '👑', status: 'online', color: '#f5b731' },
    { id: 'oracle', name: 'Oracle', role: 'Polymarket Trader',      emoji: '🔮', status: 'building', color: '#00d48a' },
  ];
}

// ─── Goals ─────────────────────────────────────────────────────────────────

function getGoals(clients) {
  const activeCount = clients.active?.length || 0;
  const mrr = clients.active?.reduce((sum, c) => sum + (c.monthlyRate || 0), 0) || 1000;
  return [
    { label: 'Active Clients', current: activeCount, target: 150, unit: '', color: '#6c63ff' },
    { label: 'Monthly Revenue', current: mrr, target: 300000, unit: '$', prefix: true, color: '#00d48a' },
    { label: 'Lead Pipeline', current: 1000, target: 5000, unit: ' leads', color: '#f5b731' },
  ];
}

// ─── Titan quote ───────────────────────────────────────────────────────────

function getTitanQuote() {
  const quotes = [
    { text: "The constraint is outreach volume. Until the SDR role is filled, everything else is optimization theater.", author: "Titan" },
    { text: "Charge more OR deliver more. Never cut price when you can add value instead.", author: "Titan via Hormozi" },
    { text: "What did you do today that a $300K/month Halo would recognize?", author: "Titan" },
    { text: "You have runway, a market, and a system. The only thing left is volume.", author: "Titan" },
    { text: "Specific knowledge + leverage = wealth. Halo is the specific knowledge. Build the leverage.", author: "Titan via Naval" },
  ];
  const day = new Date().getDay();
  return quotes[day % quotes.length];
}

// ─── API ───────────────────────────────────────────────────────────────────

app.get('/api/state', (req, res) => {
  const { wins, streak } = parseWinLog();
  const tasks = parseTodo();
  const clients = parseClients();
  const goals = getGoals(clients);
  const agents = getAgents();
  const titan = getTitanQuote();

  res.json({
    timestamp: new Date().toISOString(),
    streak,
    wins,
    tasks,
    clients,
    goals,
    agents,
    titan,
    cronSchedule: [
      { name: 'Atlas Morning Brief',    time: '9:00am ET',  icon: '☀️' },
      { name: 'Titan Challenge',         time: '10:00am ET', icon: '👑' },
      { name: 'Atlas Midday',            time: '1:00pm ET',  icon: '🕐' },
      { name: 'Atlas Evening Wrap',      time: '7:00pm ET',  icon: '🌙' },
      { name: 'Atlas Weekly Wrap',       time: 'Sun 6pm ET', icon: '📊' },
      { name: 'Titan Board Session',     time: 'Sun 6:30pm', icon: '👑' },
    ],
  });
});

app.get('/api/wins', (req, res) => {
  res.json(parseWinLog());
});

app.listen(PORT, () => {
  console.log(`Mission Control live → http://localhost:${PORT}`);
});
