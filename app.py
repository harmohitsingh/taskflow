import json
import uuid
from datetime import date, datetime
from pathlib import Path

import streamlit as st

TASKS_FILE = Path("tasks.json")

PRIORITY_META = {
    "🔴 High":   {"color": "#ef4444", "badge": "#fef2f2"},
    "🟡 Medium": {"color": "#f59e0b", "badge": "#fffbeb"},
    "🟢 Low":    {"color": "#22c55e", "badge": "#f0fdf4"},
}
CATEGORIES = ["Work", "Personal", "Shopping", "Health", "Learning", "Other"]


# ── Persistence ────────────────────────────────────────────────────────────────

def load_tasks() -> list[dict]:
    if TASKS_FILE.exists():
        try:
            return json.loads(TASKS_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
    return []


def save_tasks(tasks: list[dict]) -> None:
    TASKS_FILE.write_text(json.dumps(tasks, indent=2, ensure_ascii=False), encoding="utf-8")


# ── Session state ──────────────────────────────────────────────────────────────

if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()
if "filter" not in st.session_state:
    st.session_state.filter = "All"


# ── Mutations ──────────────────────────────────────────────────────────────────

def add_task(title: str, priority: str, category: str, due: date | None) -> None:
    title = title.strip()
    if not title:
        return
    st.session_state.tasks.append({
        "id":       str(uuid.uuid4()),
        "title":    title,
        "done":     False,
        "priority": priority,
        "category": category,
        "due":      due.isoformat() if due else None,
        "created":  datetime.now().isoformat(timespec="seconds"),
    })
    save_tasks(st.session_state.tasks)


def toggle_task(task_id: str) -> None:
    for t in st.session_state.tasks:
        if t["id"] == task_id:
            t["done"] = not t["done"]
            break
    save_tasks(st.session_state.tasks)


def delete_task(task_id: str) -> None:
    st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != task_id]
    save_tasks(st.session_state.tasks)


def clear_completed() -> None:
    st.session_state.tasks = [t for t in st.session_state.tasks if not t["done"]]
    save_tasks(st.session_state.tasks)


# ── Page config & custom CSS ───────────────────────────────────────────────────

st.set_page_config(page_title="TaskFlow", page_icon="⚡", layout="centered")

st.markdown("""
<style>
/* ── Global ── */
html, body, [data-testid="stAppViewContainer"] {
    background: #0f1117;
}
[data-testid="stAppViewContainer"] > .main {
    padding-top: 1rem;
}

/* ── Header banner ── */
.header-banner {
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #1e3a8a 100%);
    border-radius: 16px;
    padding: 28px 32px 20px;
    margin-bottom: 24px;
    border: 1px solid #3730a3;
}
.header-banner h1 {
    color: #e0e7ff;
    font-size: 2rem;
    font-weight: 800;
    margin: 0 0 4px;
    letter-spacing: -0.5px;
}
.header-banner p {
    color: #a5b4fc;
    margin: 0;
    font-size: 0.9rem;
}

/* ── Stats row ── */
.stats-row {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
}
.stat-card {
    flex: 1;
    background: #1e2030;
    border: 1px solid #2d3148;
    border-radius: 10px;
    padding: 14px 16px;
    text-align: center;
}
.stat-card .num {
    font-size: 1.6rem;
    font-weight: 700;
    color: #a5b4fc;
}
.stat-card .lbl {
    font-size: 0.72rem;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

/* ── Progress bar ── */
.progress-wrap {
    background: #1e2030;
    border-radius: 8px;
    padding: 14px 16px;
    margin-bottom: 20px;
    border: 1px solid #2d3148;
}
.progress-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.8rem;
    color: #9ca3af;
    margin-bottom: 8px;
}
.progress-bg {
    background: #374151;
    border-radius: 99px;
    height: 8px;
    overflow: hidden;
}
.progress-fill {
    height: 8px;
    border-radius: 99px;
    background: linear-gradient(90deg, #6366f1, #818cf8);
    transition: width 0.4s ease;
}

/* ── Task card ── */
.task-card {
    background: #1a1d2e;
    border: 1px solid #2d3148;
    border-left: 4px solid #6366f1;
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 8px;
    transition: border-color 0.2s;
}
.task-card.done {
    border-left-color: #374151;
    opacity: 0.55;
}
.task-title {
    font-size: 0.97rem;
    font-weight: 600;
    color: #e2e8f0;
}
.task-title.done {
    text-decoration: line-through;
    color: #6b7280;
}
.task-meta {
    display: flex;
    gap: 8px;
    margin-top: 5px;
    flex-wrap: wrap;
    align-items: center;
}
.badge {
    font-size: 0.7rem;
    padding: 2px 8px;
    border-radius: 99px;
    font-weight: 600;
}
.due-overdue { color: #f87171; font-size: 0.72rem; }
.due-ok      { color: #94a3b8; font-size: 0.72rem; }

/* ── Input area ── */
[data-testid="stForm"] {
    background: #1a1d2e;
    border: 1px solid #2d3148;
    border-radius: 12px;
    padding: 20px !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] button {
    font-size: 0.82rem !important;
}

/* ── Buttons ── */
div[data-testid="stButton"] > button {
    border-radius: 8px !important;
}

/* hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Header ─────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="header-banner">
  <h1>⚡ TaskFlow</h1>
  <p>Stay focused. Ship it. One task at a time.</p>
</div>
""", unsafe_allow_html=True)


# ── Stats ──────────────────────────────────────────────────────────────────────

tasks = st.session_state.tasks
total      = len(tasks)
done_count = sum(1 for t in tasks if t["done"])
pending    = total - done_count
pct        = int(done_count / total * 100) if total else 0

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="stat-card"><div class="num">{total}</div><div class="lbl">Total</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="stat-card"><div class="num" style="color:#86efac">{done_count}</div><div class="lbl">Completed</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="stat-card"><div class="num" style="color:#fca5a5">{pending}</div><div class="lbl">Pending</div></div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="progress-wrap">
  <div class="progress-label"><span>Overall progress</span><span>{pct}%</span></div>
  <div class="progress-bg"><div class="progress-fill" style="width:{pct}%"></div></div>
</div>
""", unsafe_allow_html=True)


# ── Add task form ──────────────────────────────────────────────────────────────

with st.expander("➕  Add a new task", expanded=not bool(tasks)):
    with st.form("add_form", clear_on_submit=True):
        title_input = st.text_input("Task title", placeholder="e.g. Finish project report…")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            priority = st.selectbox("Priority", list(PRIORITY_META.keys()), index=1)
        with col_b:
            category = st.selectbox("Category", CATEGORIES)
        with col_c:
            due = st.date_input("Due date (optional)", value=None)
        if st.form_submit_button("Add Task ⚡", use_container_width=True, type="primary"):
            if title_input.strip():
                add_task(title_input, priority, category, due)
                st.rerun()
            else:
                st.error("Task title can't be empty.")


# ── Filter tabs ────────────────────────────────────────────────────────────────

tab_all, tab_pending, tab_done = st.tabs(["All tasks", "⏳ Pending", "✅ Completed"])

def render_tasks(task_list: list[dict], ns: str) -> None:
    if not task_list:
        st.markdown('<p style="color:#6b7280;font-size:0.85rem;padding:12px 0">Nothing here yet.</p>', unsafe_allow_html=True)
        return

    for task in sorted(task_list, key=lambda t: (t["done"], list(PRIORITY_META).index(t.get("priority","🟡 Medium")))):
        tid      = task["id"]
        is_done  = task["done"]
        pri      = task.get("priority", "🟡 Medium")
        cat      = task.get("category", "Other")
        due_str  = task.get("due")
        pri_color = PRIORITY_META[pri]["color"]
        card_cls  = "task-card done" if is_done else "task-card"
        title_cls = "task-title done" if is_done else "task-title"

        # Due date badge
        due_html = ""
        if due_str:
            due_date = date.fromisoformat(due_str)
            overdue  = not is_done and due_date < date.today()
            cls      = "due-overdue" if overdue else "due-ok"
            icon     = "🔥" if overdue else "📅"
            due_html = f'<span class="{cls}">{icon} {due_date.strftime("%b %d")}</span>'

        st.markdown(f"""
        <div class="{card_cls}" style="border-left-color:{pri_color if not is_done else '#374151'}">
          <div class="{title_cls}">{task["title"]}</div>
          <div class="task-meta">
            <span class="badge" style="background:{PRIORITY_META[pri]['badge']};color:{pri_color}">{pri}</span>
            <span class="badge" style="background:#1e3a5f;color:#93c5fd">{cat}</span>
            {due_html}
          </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])
        with col1:
            label = "↩ Mark pending" if is_done else "✔ Mark done"
            if st.button(label, key=f"{ns}_tog_{tid}", use_container_width=True):
                toggle_task(tid)
                st.rerun()
        with col2:
            if st.button("🗑 Delete", key=f"{ns}_del_{tid}", use_container_width=True):
                delete_task(tid)
                st.rerun()

with tab_all:
    render_tasks(tasks, "all")

with tab_pending:
    render_tasks([t for t in tasks if not t["done"]], "pending")

with tab_done:
    render_tasks([t for t in tasks if t["done"]], "done")
    if any(t["done"] for t in tasks):
        st.divider()
        if st.button("🧹 Clear all completed", type="secondary"):
            clear_completed()
            st.rerun()
