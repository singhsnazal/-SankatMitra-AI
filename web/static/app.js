const chat = document.getElementById("chat");
const query = document.getElementById("query");
const sendBtn = document.getElementById("sendBtn");
const clearBtn = document.getElementById("clearBtn");

// 🔥 Define bot name once (easy future change)
const BOT_NAME = "SankatMitra AI";

// Professional welcome message
const WELCOME_MESSAGE =
  "Hi 👋 I’m SankatMitra AI — your AI-powered disaster preparedness and emergency response assistant. How can I assist you today?";

function timeNow() {
  const d = new Date();
  return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function bubble(text, who = "ai", sources = null) {
  const wrap = document.createElement("div");
  wrap.className = `bubble ${who}`;

  wrap.innerHTML = `
    <div>${escapeHtml(text)}</div>
    <div class="meta">${who === "user" ? "You" : BOT_NAME} • ${timeNow()}</div>
  `;

  if (sources && sources.length) {
    const s = document.createElement("div");
    s.className = "sources";
    s.innerHTML = `
      <b>📌 Sources</b>
      <ul>${sources.map(x => `<li>${escapeHtml(x)}</li>`).join("")}</ul>
    `;
    wrap.appendChild(s);
  }

  chat.appendChild(wrap);
  chat.scrollTop = chat.scrollHeight;
}

function typingIndicator() {
  const t = document.createElement("div");
  t.className = "typing";
  t.id = "typing";
  t.innerHTML = `
    <div class="dot"></div>
    <div class="dot"></div>
    <div class="dot"></div>
  `;
  chat.appendChild(t);
  chat.scrollTop = chat.scrollHeight;
}

function removeTyping() {
  const t = document.getElementById("typing");
  if (t) t.remove();
}

function escapeHtml(str) {
  return str.replace(/[&<>"']/g, m => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;"
  }[m]));
}

async function askApi(question) {
  const res = await fetch(`/ask?q=${encodeURIComponent(question)}`);
  if (!res.ok) {
    const txt = await res.text();
    throw new Error(`API Error ${res.status}: ${txt}`);
  }
  return await res.json();
}

async function send() {
  const q = query.value.trim();
  if (!q) return;

  bubble(q, "user");
  query.value = "";
  query.focus();

  typingIndicator();

  try {
    const data = await askApi(q);
    removeTyping();
    bubble(data.answer || "No answer found.", "ai", data.sources || []);
  } catch (err) {
    removeTyping();
    bubble("❌ " + err.message, "ai");
  }
}

sendBtn.addEventListener("click", send);

query.addEventListener("keydown", (e) => {
  if (e.key === "Enter") send();
});

clearBtn.addEventListener("click", () => {
  chat.innerHTML = "";
  bubble(WELCOME_MESSAGE, "ai");
});

// 🔥 Show welcome message on page load
bubble(WELCOME_MESSAGE, "ai");