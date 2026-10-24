# ⚡ TaskFlow — Personal Task Tracker

A clean, dark-themed personal task tracker built with **Python** and **Streamlit**. Add tasks, set priorities, track due dates, and mark them done — all saved locally so nothing disappears on reload.

---

## 🌐 Live Demo

👉 **[Open TaskFlow App](https://harmohitsingh-taskflow-app.streamlit.app)** *(deploy link — update after Streamlit Cloud deploy)*

---

## ✨ Features

- ✅ Add, complete, and delete tasks
- 🔴🟡🟢 Priority levels — High, Medium, Low
- 🗂️ Category tags — Work, Personal, Shopping, Health, Learning
- 📅 Due date picker with 🔥 overdue detection
- 📊 Live progress bar + stats (Total / Completed / Pending)
- 🗃️ Filter tabs — All, Pending, Completed
- 🧹 Bulk clear completed tasks
- 💾 Persists tasks to `tasks.json` — survives app restarts

---


---

## 🚀 Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/harmohitsingh/taskflow.git
cd taskflow
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

App opens at **http://localhost:8501**

---

## 📁 Project Structure

```
taskflow/
├── app.py             # Main Streamlit application
├── requirements.txt   # Python dependencies
├── tasks.json         # Local task storage (auto-created, gitignored)
└── README.md          # This file
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| [Python 3.10+](https://python.org) | Core language |
| [Streamlit](https://streamlit.io) | Web UI framework |
| JSON | Local data persistence |

---

## 👤 Author

**Harmohit Singh**
- GitHub: [@HarmohitSingh2005](https://github.com/HarmohitSingh2005)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
