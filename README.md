Gradebook (Python + Vercel)

A tiny student gradebook that stores data in the browser (localStorage) and uses serverless Python (Flask) functions to compute reports (averages, subject averages, rankings, full student report). 
🚀 Demo

App: https://gradebook-one.vercel.app/

Health check: https://gradebook-one.vercel.app//api/ping

✨ Features

Add students, subjects, and grades (0–100)

View a live table of your data

Compute:

Student Average

Subject Average (per student)

Rank Students

Full Student Report (per-subject + overall)

Data persists locally (no backend DB)

Deployed as Vercel Python Functions (one file per endpoint)

🧰 Tech Stack

Frontend: HTML + vanilla JS (index.html, app.js)

Backend: Python Flask serverless functions under /api

Hosting: Vercel (no vercel.json required)


📦 Project Structure
.
├─ api/
│  ├─ __init__.py               # makes /api importable (empty file)
│  ├─ _core.py                  # shared math helpers (avg, rank, report)
│  ├─ ping.py                   # GET  /api/ping
│  ├─ student_avg.py            # POST /api/student_avg
│  ├─ subject_avg.py            # POST /api/subject_avg
│  ├─ students_rank.py          # POST /api/students_rank
│  └─ full_student_data.py      # POST /api/full_student_data
├─ index.html                   # UI (CSP added)
├─ app.js                       # UI logic + API calls (XSS-safe rendering)
├─ requirements.txt             # Flask==3.0.3
└─ .gitignore                   # ignores .venv, __pycache__, editors, etc.

🔐 Security Notes

XSS hardened UI: no innerHTML with user input; we build DOM nodes and set textContent.

Strict CSP in index.html

Same-origin only: no CORS; the frontend and API share the same origin.

Input validation (optional upgrade): you can add size/value checks in _core.py to reject oversized or invalid payloads (e.g., grade range 0–100).

🧪 API Reference (Serverless Functions)

Each file in /api = one function at /api/<filename>.

Health

GET /api/ping → { "ok": true, "fn": "ping" }
