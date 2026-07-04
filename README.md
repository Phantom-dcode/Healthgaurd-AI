<div align="center">

# 🏥 HealthGuard AI
### AI-Powered Remote Patient Monitoring Platform

[![CI](https://github.com/Phantom-dcode/HealthGuard-AI/actions/workflows/ci.yml/badge.svg)](https://github.com/Phantom-dcode/HealthGuard-AI/actions)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)](https://reactjs.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)](https://docker.com)

*Built by [Logesh Kumar](https://github.com/Phantom-dcode)*

</div>

---

## 🚀 What is HealthGuard AI?

HealthGuard AI is a **full-stack AI-powered remote patient monitoring platform** that enables patients to track their vitals, doctors to monitor assigned patients in real time, and an AI model to predict health risks — all in a beautiful, dark-themed dashboard.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 **JWT Auth** | Secure login with access + refresh tokens |
| 👤 **3 Role System** | Patient, Doctor, Admin with full RBAC |
| 📊 **Vitals Tracking** | BP, Heart Rate, Blood Sugar, SpO2, Temp, Weight |
| 🤖 **AI Risk Prediction** | Scikit-Learn ML model scores health risk (Low/Medium/High) |
| 🚨 **Auto Alerts** | Real-time alerts when vitals exceed clinical thresholds |
| 📈 **Charts** | Line charts for trend analysis, Risk gauge |
| 📋 **Reports** | Doctor-generated patient health reports |
| 🔍 **Audit Logs** | Immutable trail of all system actions (Admin) |
| 🌙 **Dark Mode UI** | Professional healthcare SaaS dark theme |
| 🐳 **Docker Ready** | One command to run the full stack |

---

## 🛠️ Tech Stack

```
Backend   →  FastAPI + SQLAlchemy + PostgreSQL + JWT + Scikit-Learn
Frontend  →  React 18 + Vite + Tailwind CSS + Framer Motion + Chart.js
DevOps    →  Docker + GitHub Actions + AWS (ECS + S3 + CloudFront)
```

---

## ⚡ Quick Start (Docker)

```bash
# 1. Clone
git clone https://github.com/Phantom-dcode/HealthGuard-AI.git
cd HealthGuard-AI

# 2. Start everything
cd backend
cp .env.example .env          # edit your SECRET_KEY
docker-compose up --build

# 3. Frontend (separate terminal)
cd frontend
npm install
cp .env.example .env
npm run dev
```

**Open:** `http://localhost:5173`
**API Docs:** `http://localhost:8000/docs`

---

## 🔑 Demo Login

| Role | Email | Password |
|---|---|---|
| Admin | admin@healthguard.ai | Admin@123 |
| Register | /register | Choose Patient or Doctor |

---

## 📁 Project Structure

```
HealthGuard-AI/
├── backend/          # FastAPI + PostgreSQL + ML
│   ├── app/
│   │   ├── models/   # SQLAlchemy ORM
│   │   ├── schemas/  # Pydantic validation
│   │   ├── routers/  # API endpoints
│   │   ├── services/ # Business logic + ML
│   │   └── core/     # Security + Logging
│   └── Dockerfile
├── frontend/         # React + Tailwind
│   └── src/
│       ├── pages/    # Patient / Doctor / Admin dashboards
│       ├── components/
│       └── api/      # Axios API clients
└── .github/
    └── workflows/    # CI/CD pipelines
```

---

## 📡 API Endpoints

```
POST /api/v1/auth/register    → Register new user
POST /api/v1/auth/login       → Get JWT tokens
GET  /api/v1/patients/me      → Patient profile
POST /api/v1/health-records   → Submit vitals (auto-alerts + AI prediction)
GET  /api/v1/alerts           → View alerts
POST /api/v1/predictions/predict → Run AI risk model
GET  /api/v1/audit-logs       → Admin audit trail
```
Full docs at `/docs` (Swagger UI auto-generated)

---

## 👨‍💻 Developer

**Logesh Kumar** — B.E. CSE (AI & ML), KPRIET Coimbatore
- GitHub: [@Phantom-dcode](https://github.com/Phantom-dcode)
- Fiverr: [logesh911](https://fiverr.com/logesh911)

---

<div align="center">
Built with ❤️ using FastAPI, React, and AI
</div>
