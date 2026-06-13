// filepath: fe/app.js
// Crowdjump dev web client. Vanilla JS, no build step. A thin client of the
// REST API that mimics the Telegram bot's flows; wording copies
// src/bot/texts.py so web and bot stay in sync by eye.

"use strict";

const API_BASE = localStorage.getItem("cj_api") || "http://localhost:8000";
const TG_FILE_LIMIT_MB = 20; // mirror of Settings.TG_FILE_LIMIT_MB
const POLL_MS = 8000;

const state = {
  access: localStorage.getItem("cj_access"),
  refresh: localStorage.getItem("cj_refresh"),
  me: null,
  wizard: null, // {type: "launch"|"phone", step, data}
  lastNotifId: 0,
  pollTimer: null,
  submitTaskId: null,
};

// --- tiny DOM helpers -------------------------------------------------------

const $ = (id) => document.getElementById(id);
const chat = () => $("chat");

function esc(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  })[c]);
}

function scrollDown() {
  chat().scrollTop = chat().scrollHeight;
}

function bubble(html, cls) {
  const div = document.createElement("div");
  div.className = `msg ${cls}`;
  div.innerHTML = html;
  chat().appendChild(div);
  scrollDown();
  return div;
}

const botMsg = (html) => bubble(html, "bot");
const userMsg = (text) => bubble(esc(text), "user");
const errMsg = (text) => bubble(esc(text), "err");
const bellMsg = (text) => bubble("🔔 " + esc(text), "bell");

// keyboard: rows of {label, cb}. One-shot: greys out after any click.
function keyboard(rows) {
  const kb = document.createElement("div");
  kb.className = "kb";
  for (const row of rows) {
    const rowEl = document.createElement("div");
    rowEl.className = "row";
    for (const btn of row) {
      const b = document.createElement("button");
      b.textContent = btn.label;
      b.onclick = () => {
        if (kb.classList.contains("used")) return;
        kb.classList.add("used");
        btn.cb();
      };
      rowEl.appendChild(b);
    }
    kb.appendChild(rowEl);
  }
  chat().appendChild(kb);
  scrollDown();
  return kb;
}

// --- API client (mirror of bot/api_client.py) -------------------------------

function flattenDetail(detail) {
  if (Array.isArray(detail)) {
    return detail
      .map((e) => {
        const loc = (e.loc || []).filter((x) => x !== "body").join(".");
        return `${loc}: ${e.msg || ""}`.replace(/^: /, "");
      })
      .join("; ");
  }
  return String(detail);
}

async function api(path, { method = "GET", body, raw = false } = {}) {
  const doFetch = () =>
    fetch(API_BASE + path, {
      method,
      headers: {
        "Content-Type": "application/json",
        ...(state.access ? { Authorization: `Bearer ${state.access}` } : {}),
      },
      body: body === undefined ? undefined : JSON.stringify(body),
    });

  let resp;
  try {
    resp = await doFetch();
    if (resp.status === 401 && state.refresh && path !== "/auth/refresh") {
      const ok = await tryRefresh();
      if (!ok) { logout(); throw { status: 401, detail: "Session expired — log in again" }; }
      resp = await doFetch();
    }
  } catch (e) {
    if (e && e.status) throw e;
    throw { status: 0, detail: "backend unreachable — is the API running on " + API_BASE + "?" };
  }

  if (!resp.ok) {
    let detail = resp.statusText;
    try { detail = flattenDetail((await resp.json()).detail); } catch (_) { /* keep statusText */ }
    throw { status: resp.status, detail };
  }
  return raw ? resp : resp.json();
}

async function tryRefresh() {
  try {
    const r = await fetch(API_BASE + "/auth/refresh", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh_token: state.refresh }),
    });
    if (!r.ok) return false;
    setTokens(await r.json());
    return true;
  } catch (_) {
    return false;
  }
}

function setTokens(pair) {
  state.access = pair.access_token;
  state.refresh = pair.refresh_token;
  localStorage.setItem("cj_access", state.access);
  localStorage.setItem("cj_refresh", state.refresh);
}

function friendly(e) {
  return e.status === 0 ? e.detail : `Can't do that: ${e.detail}`;
}

// --- auth -------------------------------------------------------------------

async function login(register) {
  const email = $("email").value.trim();
  const password = $("password").value;
  $("login-error").textContent = "";
  try {
    const pair = register
      ? await api("/auth/register", { method: "POST", body: { email, password } })
      : await api("/auth/login", { method: "POST", body: { email, password } });
    setTokens(pair);
    await afterAuth();
  } catch (e) {
    $("login-error").textContent = e.detail;
  }
}

function logout() {
  localStorage.removeItem("cj_access");
  localStorage.removeItem("cj_refresh");
  state.access = state.refresh = state.me = null;
  state.wizard = null;
  if (state.pollTimer) clearInterval(state.pollTimer);
  $("frame").classList.add("hidden");
  $("login").classList.remove("hidden");
}

async function afterAuth() {
  state.me = await api("/users/me");
  $("login").classList.add("hidden");
  $("frame").classList.remove("hidden");
  $("who").textContent = state.me.email || `tg:${state.me.telegram_handle || state.me.id}`;
  chat().innerHTML = "";
  showMenu();
  startPolling();
}

// --- menu & commands ----------------------------------------------------------

const HELP =
  "<b>Crowdjump</b> — launch a task, the crowd jumps on it.\n\n" +
  "/launch — create a task (you pay, Jumpers perform)\n" +
  "/browse — see open tasks you can jump on\n" +
  "/mytasks — tasks you launched\n" +
  "/myjumps — tasks you jumped on\n" +
  "/profile — account & verification\n" +
  "/cancel — abort the current flow";

function showMenu() {
  botMsg(
    "Welcome to <b>Crowdjump</b>!\n\nLaunch a task — the crowd jumps on it.\n" +
      "Earn money by jumping on tasks that match you.\n\nWhat would you like to do?"
  );
  keyboard([
    [{ label: "🚀 Launch a task", cb: startLaunch }],
    [{ label: "👀 Browse tasks", cb: () => browse(1) }],
    [
      { label: "📋 My tasks", cb: myTasks },
      { label: "🐦 My jumps", cb: myJumps },
    ],
    [
      { label: "👤 Profile", cb: profile },
      { label: "❓ Help", cb: () => botMsg(HELP) },
    ],
  ]);
}

function handleCommand(text) {
  const cmd = text.split(/\s/)[0].toLowerCase();
  const actions = {
    "/start": () => { state.wizard = null; showMenu(); },
    "/help": () => botMsg(HELP),
    "/cancel": cancelFlow,
    "/launch": startLaunch,
    "/browse": () => browse(1),
    "/mytasks": myTasks,
    "/myjumps": myJumps,
    "/profile": profile,
  };
  (actions[cmd] || (() => botMsg("Unknown command — try /help")))();
}

function cancelFlow() {
  if (!state.wizard) {
    botMsg("Nothing in progress. /start for the menu.");
    return;
  }
  state.wizard = null;
  botMsg("Cancelled. Back to the main menu: /start");
}

async function onInput() {
  const text = $("cmd").value.trim();
  if (!text) return;
  $("cmd").value = "";
  userMsg(text);
  if (text.startsWith("/")) return handleCommand(text);
  if (state.wizard) return wizardInput(text);
  botMsg("Pick something from the menu, or /help");
}

// --- launch wizard (mirror of bot/flows/launch.py) ---------------------------

function startLaunch() {
  state.wizard = { type: "launch", step: "desc", data: {} };
  botMsg("<b>Step 1/6 · Description</b>\nWhat should Jumpers do? Describe the task in your own words.");
  cancelKb();
}

function cancelKb() {
  keyboard([[{ label: "✖️ Cancel", cb: cancelFlow }]]);
}

const parseNum = (t) => {
  const v = parseFloat(t.replace(",", "."));
  return Number.isFinite(v) && v > 0 ? v : null;
};

function parseAge(t) {
  if (t === "skip") return [null, null];
  if (!t.includes("-")) return null;
  const [loS, hiS] = t.split("-", 2);
  const lo = loS ? parseInt(loS, 10) : null;
  const hi = hiS ? parseInt(hiS, 10) : null;
  if ((loS && !Number.isInteger(lo)) || (hiS && !Number.isInteger(hi))) return null;
  if (lo !== null && hi !== null && lo > hi) return null;
  for (const v of [lo, hi]) if (v !== null && (v < 0 || v > 130)) return null;
  return [lo, hi];
}

async function wizardInput(text) {
  const w = state.wizard;
  if (w.type === "phone") return phoneInput(text);
  if (w.type !== "launch") return;

  const steps = {
    desc() {
      if (text.length < 1 || text.length > 5000)
        return reask("Please describe the task in 1–5000 characters.");
      w.data.desc = text;
      next("budget", "<b>Step 2/6 · Budget</b>\nTotal budget for this task, in USDT (just a number, e.g. 50):");
    },
    budget() {
      const v = parseNum(text);
      if (v === null) return reask("That doesn't look like a positive number — try again (e.g. 50):");
      w.data.budget = v;
      next("you_earn", "<b>Step 2/6 · Pay</b>\nHow much does each Jumper earn? (e.g. 5)");
    },
    you_earn() {
      const v = parseNum(text);
      if (v === null) return reask("That doesn't look like a positive number — try again (e.g. 5):");
      if (v > w.data.budget)
        return reask(`A single Jumper can't earn more than the whole budget (${w.data.budget}). Try a smaller number:`);
      w.data.you_earn = v;
      next("num_jumpers", "<b>Step 2/6 · Jumpers</b>\nHow many Jumpers do you need? (e.g. 10)");
    },
    num_jumpers() {
      const v = parseInt(text, 10);
      if (!Number.isInteger(v) || v < 1 || v > 10000)
        return reask("Give me a whole number between 1 and 10000:");
      const total = w.data.you_earn * v;
      if (total > w.data.budget) {
        const max = Math.floor(w.data.budget / w.data.you_earn);
        return reask(
          `That needs ${total} total but your budget is ${w.data.budget}.\n` +
            `With this pay you can afford at most ${max} Jumpers — enter a smaller count:`
        );
      }
      w.data.num_jumpers = v;
      w.step = "location";
      botMsg(
        "<b>Step 3/6 · Filters — location</b>\nWhere should Jumpers be from? Type it freely " +
          "(e.g. <i>Germany</i>, <i>Istanbul</i>, <i>EMEA but not Russia</i>) — or skip:"
      );
      keyboard([
        [{ label: "🌍 Anywhere (skip)", cb: () => locationChosen(null) }],
        [{ label: "✖️ Cancel", cb: cancelFlow }],
      ]);
    },
    location() {
      locationChosen(text.slice(0, 200));
    },
    age() {
      const parsed = parseAge(text);
      if (parsed === null) {
        botMsg("Type an age range like <i>21-30</i> (or <i>18-</i> for 18+), or pick a button:");
        return ageKb();
      }
      ageChosen(parsed[0], parsed[1]);
    },
    deadline() {
      const days = parseInt(text, 10);
      if (!Number.isInteger(days) || days < 1 || days > 365) {
        botMsg("A whole number of days between 1 and 365, or skip:");
        return deadlineKb();
      }
      w.data.deadline_days = days;
      askManual();
    },
  };

  const fn = steps[w.step];
  if (fn) fn();
  else botMsg("Use the buttons above, or /cancel");

  function reask(msg) {
    botMsg(msg);
    cancelKb();
  }
  function next(step, prompt) {
    w.step = step;
    botMsg(prompt);
    cancelKb();
  }
}

function locationChosen(raw) {
  const w = state.wizard;
  if (!w) return;
  if (raw) w.data.location_raw = raw;
  w.step = "age";
  botMsg("<b>Step 3/6 · Filters — age</b>\nPick a range or type one like <i>21-30</i>:");
  ageKb();
}

function ageKb() {
  keyboard([
    [
      { label: "18–25", cb: () => ageChosen(18, 25) },
      { label: "25–35", cb: () => ageChosen(25, 35) },
    ],
    [
      { label: "18+", cb: () => ageChosen(18, null) },
      { label: "Any age (skip)", cb: () => ageChosen(null, null) },
    ],
    [{ label: "✖️ Cancel", cb: cancelFlow }],
  ]);
}

function ageChosen(lo, hi) {
  const w = state.wizard;
  if (!w) return;
  if (lo !== null) w.data.age_min = lo;
  if (hi !== null) w.data.age_max = hi;
  w.step = "gender";
  botMsg("<b>Step 3/6 · Filters — gender</b>");
  keyboard([
    [
      { label: "Female", cb: () => genderChosen("female") },
      { label: "Male", cb: () => genderChosen("male") },
      { label: "Any (skip)", cb: () => genderChosen(null) },
    ],
    [{ label: "✖️ Cancel", cb: cancelFlow }],
  ]);
}

function genderChosen(g) {
  const w = state.wizard;
  if (!w) return;
  if (g) w.data.gender = g;
  w.step = "deadline";
  botMsg("<b>Step 4/6 · Deadline</b>\nIn how many days must submissions be done? Type a number of days, or skip:");
  deadlineKb();
}

function deadlineKb() {
  keyboard([
    [{ label: "No deadline (skip)", cb: askManual }],
    [{ label: "✖️ Cancel", cb: cancelFlow }],
  ]);
}

function askManual() {
  const w = state.wizard;
  if (!w) return;
  w.step = "manual";
  botMsg("<b>Step 5/6 · Jumper approval</b>\nAuto-accept anyone who matches, or approve each Jumper yourself?");
  keyboard([
    [{ label: "⚡ Auto-accept Jumpers", cb: () => manualChosen(false) }],
    [{ label: "✅ I'll approve each Jumper", cb: () => manualChosen(true) }],
    [{ label: "✖️ Cancel", cb: cancelFlow }],
  ]);
}

function buildPayload(d) {
  const basic = {};
  if (d.location_raw) basic.location_filter = { raw_statement: d.location_raw };
  if (d.age_min !== undefined || d.age_max !== undefined) {
    basic.age_range = {};
    if (d.age_min !== undefined) basic.age_range.min = d.age_min;
    if (d.age_max !== undefined) basic.age_range.max = d.age_max;
  }
  if (d.gender) basic.gender = d.gender;

  const payload = {
    desc: d.desc,
    total_budget: d.budget,
    you_earn: d.you_earn,
    num_jumpers: d.num_jumpers,
    accept_jumpers_manually: !!d.manual,
  };
  if (Object.keys(basic).length) payload.filters = { basic_filters: basic };
  if (d.deadline_days) {
    const dl = new Date(Date.now() + d.deadline_days * 86400_000);
    payload.submission_deadline = dl.toISOString();
  }
  return payload;
}

async function manualChosen(manual) {
  const w = state.wizard;
  if (!w) return;
  w.data.manual = manual;
  w.step = "confirm";

  const d = w.data;
  const parts = [];
  if (d.location_raw) parts.push(`location: ${d.location_raw}`);
  if (d.age_min !== undefined || d.age_max !== undefined)
    parts.push(`age ${d.age_min ?? ""}–${d.age_max ?? ""}`.replace(/–$/, "+"));
  if (d.gender) parts.push(d.gender);

  let audienceLine = "";
  try {
    const preview = await api("/tasks/audience-preview", {
      method: "POST",
      body: { filters: buildPayload(d).filters || null },
    });
    audienceLine = `\n👥 Verified Jumpers matching right now: <b>${esc(preview.display)}</b>`;
    for (const warning of preview.warnings || []) audienceLine += `\n⚠️ <i>${esc(warning)}</i>`;
  } catch (_) { /* preview is decorative */ }

  botMsg(
    "<b>Step 6/6 · Confirm your task</b>\n\n" +
      `📝 ${esc(d.desc)}\n\n` +
      `💰 Budget: ${d.budget} USDT\n` +
      `🐦 ${d.num_jumpers} Jumper(s) × ${d.you_earn} USDT\n` +
      `🎯 Who: ${esc(parts.join(", ") || "anyone")}\n` +
      `⏰ Deadline: ${d.deadline_days ? d.deadline_days + " days" : "none"}\n` +
      `✅ Mode: ${manual ? "manual approval" : "auto-accept"}\n` +
      audienceLine +
      "\n\nLaunch it?"
  );
  keyboard([
    [{ label: "🚀 Launch it", cb: confirmLaunch }],
    [{ label: "↩️ Start over", cb: startLaunch }],
    [{ label: "✖️ Cancel", cb: cancelFlow }],
  ]);
}

async function confirmLaunch() {
  const w = state.wizard;
  if (!w || w.step !== "confirm") return;
  try {
    const task = await api("/tasks", { method: "POST", body: buildPayload(w.data) });
    state.wizard = null;
    botMsg(
      `🚀 <b>Task #${task.id} launched!</b>\nIt's now visible to Jumpers (${task.num_jumpers} slot(s)).\n\n` +
        "<i>Escrow funding arrives with the payments component — for now tasks launch unfunded in this dev build.</i>"
    );
    showMenu();
  } catch (e) {
    errMsg(friendly(e));
  }
}

// --- browse -------------------------------------------------------------------

async function browse(page) {
  try {
    const data = await api(`/tasks?status=open&page=${page}&size=1`);
    if (!data.total || !data.items.length) {
      botMsg("No open tasks right now — check back soon!");
      return;
    }
    const t = data.items[0];
    botMsg(
      `<b>Task ${page} of ${data.total}</b>\n\n` +
        `📝 ${esc(t.desc.slice(0, 300))}\n\n` +
        `💵 You earn: <b>${t.you_earn} USDT</b>\n` +
        `🐦 Slots: ${t.num_jumpers}\n` +
        `🏷 Category: ${esc(t.category || "general")}\n` +
        `✅ ${t.accept_jumpers_manually ? "manual approval" : "auto-accept"}`
    );
    const nav = [];
    if (page > 1) nav.push({ label: "⬅️ Prev", cb: () => browse(page - 1) });
    if (page < data.total) nav.push({ label: "Next ➡️", cb: () => browse(page + 1) });
    const rows = [];
    if (nav.length) rows.push(nav);
    rows.push([{ label: "🐦 Jump on this", cb: () => jump(t.id, page) }]);
    rows.push([{ label: "↩️ Menu", cb: showMenu }]);
    keyboard(rows);
  } catch (e) {
    errMsg(friendly(e));
  }
}

async function jump(taskId, page) {
  try {
    const j = await api(`/tasks/${taskId}/jump`, { method: "POST" });
    botMsg(
      j.status === "pending"
        ? `⏳ Application sent for task <b>#${taskId}</b> — the Launcher approves Jumpers manually. You'll see the result in /myjumps.`
        : `🐦 You're on task <b>#${taskId}</b>! Perform it while screen-recording, then submit your proof from /myjumps.`
    );
    browse(page);
  } catch (e) {
    errMsg(friendly(e));
  }
}

// --- my jumps -------------------------------------------------------------------

const STATUS_EMOJI = {
  pending: "⏳", active: "🏃", submitted: "📨",
  verified: "✅", rejected: "❌", forfeited: "🏳️",
};

async function myJumps() {
  try {
    const parts = await api("/tasks/participated");
    if (!parts.length) {
      botMsg("You haven't jumped on anything yet. Try /browse!");
      return;
    }
    const lines = ["<b>Your jumps</b>"];
    const rows = [];
    for (const p of parts.slice(0, 10)) {
      const e = STATUS_EMOJI[p.jump.status] || "▫️";
      lines.push(
        `${e} <b>#${p.task.id}</b> ${esc(p.task.desc.slice(0, 60))} — ${p.task.you_earn} USDT · <i>${p.jump.status}</i>`
      );
      const row = [];
      if (["pending", "active"].includes(p.jump.status))
        row.push({ label: `🏳️ Forfeit #${p.task.id}`, cb: () => forfeit(p.task.id) });
      if (p.jump.status === "active")
        row.push({ label: `📤 Submit proof #${p.task.id}`, cb: () => submitProof(p.task.id) });
      if (row.length) rows.push(row);
    }
    botMsg(lines.join("\n"));
    if (rows.length) keyboard(rows);
  } catch (e) {
    errMsg(friendly(e));
  }
}

async function forfeit(taskId) {
  try {
    await api(`/tasks/${taskId}/forfeit`, { method: "POST" });
    botMsg(`🏳️ You backed out of task #${taskId}. The slot is free again.`);
    myJumps();
  } catch (e) {
    errMsg(friendly(e));
  }
}

function submitProof(taskId) {
  state.submitTaskId = taskId;
  botMsg(
    `📤 <b>Submit proof for task #${taskId}</b>\nPick your screen recording (up to ${TG_FILE_LIMIT_MB} MB).`
  );
  $("proofFile").click();
}

function onProofPicked() {
  const file = $("proofFile").files[0];
  $("proofFile").value = "";
  if (!file || state.submitTaskId === null) return;
  const sizeMb = file.size / (1024 * 1024);
  if (sizeMb > TG_FILE_LIMIT_MB) {
    errMsg(
      `That file is ${sizeMb.toFixed(1)} MB — I can only take up to ${TG_FILE_LIMIT_MB} MB right now.\n` +
        "Tips: trim the recording to just the task, or export at 720p. Then pick it again."
    );
    return;
  }
  botMsg(
    `📨 Got your recording for task #${state.submitTaskId}!\n` +
      "<i>Verification is coming soon in this dev build — the file was not stored yet, and your jump stays active.</i>"
  );
  state.submitTaskId = null;
}

// --- my tasks (Launcher) ----------------------------------------------------------

const TASK_EMOJI = { open: "🟢", full: "🔵", completed: "✅", cancelled: "⚫", disputed: "⚠️", draft: "📝" };

async function myTasks() {
  try {
    const tasks = await api("/tasks/my");
    if (!tasks.length) {
      botMsg("You haven't launched anything yet. Try /launch!");
      return;
    }
    const lines = ["<b>Your launched tasks</b>"];
    const rows = [];
    for (const t of tasks.slice(0, 10)) {
      lines.push(
        `${TASK_EMOJI[t.status] || "▫️"} <b>#${t.id}</b> ${esc(t.desc.slice(0, 60))} — ${t.num_jumpers} slot(s) · <i>${t.status}</i>`
      );
      rows.push([{ label: `👥 Jumpers of #${t.id}`, cb: () => taskJumps(t.id) }]);
    }
    botMsg(lines.join("\n"));
    keyboard(rows);
  } catch (e) {
    errMsg(friendly(e));
  }
}

async function taskJumps(taskId) {
  try {
    const jumps = await api(`/tasks/${taskId}/jumps`);
    if (!jumps.length) {
      botMsg(`Task #${taskId} has no Jumpers yet.`);
      return;
    }
    const lines = [`<b>Jumpers of task #${taskId}</b>`];
    const rows = [];
    for (const j of jumps) {
      lines.push(`${STATUS_EMOJI[j.status] || "▫️"} Jumper ${j.jumper_id} — <i>${j.status}</i>`);
      if (j.status === "pending")
        rows.push([
          { label: `✅ Approve ${j.jumper_id}`, cb: () => decide(taskId, j.id, true) },
          { label: `❌ Decline ${j.jumper_id}`, cb: () => decide(taskId, j.id, false) },
        ]);
    }
    botMsg(lines.join("\n"));
    if (rows.length) keyboard(rows);
  } catch (e) {
    errMsg(friendly(e));
  }
}

async function decide(taskId, jumpId, approve) {
  try {
    await api(`/tasks/${taskId}/jumps/${jumpId}/${approve ? "approve" : "reject"}`, { method: "POST" });
    botMsg(approve ? "Approved ✅" : "Declined");
    taskJumps(taskId);
  } catch (e) {
    errMsg(friendly(e));
  }
}

// --- profile + phone wizard -------------------------------------------------------

async function profile() {
  try {
    const me = (state.me = await api("/users/me"));
    const verifs = (me.verifications || [])
      .map((v) => `${v.verification_name} (${v.status})`)
      .join(", ") || "none yet";
    botMsg(
      "<b>Your profile</b>\n" +
        `Email: ${esc(me.email || "—")} ${me.email ? (me.is_email_verified ? "✅" : "(unverified)") : ""}\n` +
        `Phone: ${esc(me.phone_number || "—")} ${me.is_phone_verified ? "✅" : ""}\n` +
        `Verifications: ${esc(verifs)}\n` +
        `Trust score: ${me.trust_score ?? "—"}\n` +
        `Notifications: ${me.notifications_muted ? "muted 🔕" : "on 🔔"}`
    );
    const rows = [];
    if (me.email && !me.is_email_verified)
      rows.push([{ label: "📧 Resend verification email", cb: resendVerification }]);
    if (!me.is_phone_verified)
      rows.push([{ label: "📱 Verify phone", cb: startPhoneWizard }]);
    rows.push([
      {
        label: me.notifications_muted ? "🔔 Unmute notifications" : "🔕 Mute notifications",
        cb: () => setMute(!me.notifications_muted),
      },
    ]);
    keyboard(rows);
  } catch (e) {
    errMsg(friendly(e));
  }
}

async function resendVerification() {
  try {
    const r = await api("/auth/resend-verification", { method: "POST" });
    botMsg(esc(r.msg) + "\n<i>Dev tip: the link is in the API console (console email backend).</i>");
  } catch (e) {
    errMsg(friendly(e));
  }
}

async function setMute(muted) {
  try {
    await api("/users/me/notifications", { method: "POST", body: { muted } });
    botMsg(muted ? "Notifications muted 🔕" : "Notifications on 🔔");
    profile();
  } catch (e) {
    errMsg(friendly(e));
  }
}

function startPhoneWizard() {
  state.wizard = { type: "phone", step: "number", data: {} };
  botMsg("📱 Send your phone number in international format, e.g. <i>+49 170 1234567</i>");
  cancelKb();
}

async function phoneInput(text) {
  const w = state.wizard;
  if (w.step === "number") {
    try {
      await api("/auth/phone/request", { method: "POST", body: { phone_number: text } });
      w.step = "code";
      botMsg(
        "Code sent! Enter the 6-digit code.\n" +
          "<i>Dev tip: mock Twilio prints the code in the API console.</i>"
      );
      cancelKb();
    } catch (e) {
      errMsg(friendly(e));
      cancelKb();
    }
  } else if (w.step === "code") {
    try {
      await api("/auth/phone/verify", { method: "POST", body: { code: text } });
      state.wizard = null;
      botMsg("📱 Phone verified ✅");
      profile();
    } catch (e) {
      errMsg(friendly(e));
      cancelKb();
    }
  }
}

// --- notifications polling ----------------------------------------------------------

function startPolling() {
  if (state.pollTimer) clearInterval(state.pollTimer);
  state.lastNotifId = 0;
  // first poll primes since_id without replaying history
  api("/users/me/notifications?limit=1")
    .then((rows) => { if (rows.length) state.lastNotifId = rows[0].id; })
    .catch(() => {});
  state.pollTimer = setInterval(pollNotifications, POLL_MS);
}

async function pollNotifications() {
  if (!state.access) return;
  try {
    const rows = await api(`/users/me/notifications?since_id=${state.lastNotifId}`);
    for (const row of rows.reverse()) {
      // oldest first
      state.lastNotifId = Math.max(state.lastNotifId, row.id);
      if (row.text && row.status === "sent") bellMsg(row.text);
    }
  } catch (_) { /* polling never bothers the user */ }
}

// --- wire-up ---------------------------------------------------------------------

$("btn-login").onclick = () => login(false);
$("btn-register").onclick = () => login(true);
$("btn-logout").onclick = logout;
$("send").onclick = onInput;
$("cmd").addEventListener("keydown", (e) => { if (e.key === "Enter") onInput(); });
$("password").addEventListener("keydown", (e) => { if (e.key === "Enter") login(false); });
$("proofFile").addEventListener("change", onProofPicked);

if (state.access) {
  afterAuth().catch(() => logout());
}
