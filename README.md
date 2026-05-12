# IPL Prediction League Dashboard

Modern IPL prediction leaderboard dashboard with live Cricinfo results.

## Features

- Live IPL winner fetch via Cricinfo (`cricdata`)
- Embedded prediction responses (no Excel runtime dependency)
- Leaderboard scoring
- Accuracy %
- Match timeline with per-person correctness
- Team popularity analytics
- Biggest upset detection
- Longest streak tracking
- Modern dark glassmorphism dashboard
- Localhost ready
- Deployable to Render / Railway / Fly.io

---

## Project structure

```bash
ipl-leaderboard/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── responses.py
├── services/
│   ├── cricket_service.py
│   ├── scoring_service.py
│   └── stats_service.py
├── templates/
│   └── index.html
└── static/
    ├── styles.css
    └── dashboard.js