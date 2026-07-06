<div align="center">

# 🏥 HealthGuard AI
## AI-Powered Remote Patient Monitoring Platform

<p>
  <a href="https://github.com/Phantom-dcode/Healthgaurd-AI/stargazers">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/Phantom-dcode/Healthgaurd-AI?style=for-the-badge&color=0EA5E9">
  </a>
  <a href="https://github.com/Phantom-dcode/Healthgaurd-AI/network/members">
    <img alt="GitHub forks" src="https://img.shields.io/github/forks/Phantom-dcode/Healthgaurd-AI?style=for-the-badge&color=10B981">
  </a>
  <a href="https://github.com/Phantom-dcode/Healthgaurd-AI/issues">
    <img alt="GitHub issues" src="https://img.shields.io/github/issues/Phantom-dcode/Healthgaurd-AI?style=for-the-badge&color=EF4444">
  </a>
  <a href="LICENSE">
    <img alt="MIT License" src="https://img.shields.io/badge/license-MIT-purple?style=for-the-badge">
  </a>
</p>

**Enterprise-Grade Healthcare Platform**  
*Enabling Remote Patient Monitoring with AI-Powered Health Risk Prediction*

[🚀 Live Demo](#live-demo) • [📖 Documentation](#documentation) • [🐛 Report Bug](#support) • [💡 Request Feature](#support)

</div>

---

## ✨ Platform Overview

HealthGuard AI is a **production-ready, full-stack healthcare monitoring platform** that revolutionizes patient care through intelligent monitoring and predictive analytics.

### 🎯 Key Capabilities

| Feature | Description | Impact |
|---------|-------------|--------|
| **🔐 Enterprise Security** | JWT-based auth with role-based access (RBAC) | 3 secure portals (Patient/Doctor/Admin) |
| **📊 Real-Time Vitals** | Monitor 6+ vital signs with instant thresholds | Auto-alerts when values exceed clinical limits |
| **🤖 AI Risk Prediction** | Scikit-Learn ML model analyzes health patterns | Predicts disease risk (Low/Medium/High) |
| **📈 Visual Analytics** | Interactive charts, risk gauges, trend analysis | Actionable insights at a glance |
| **🏥 Doctor Workflows** | Assign patients, view dashboards, generate reports | Streamlined patient management |
| **📋 Audit Trail** | Immutable logs of all system actions | Full regulatory compliance |
| **🌙 Professional UI** | Dark-themed SaaS dashboard with animations | Enterprise-grade aesthetics |
| **🐳 Cloud Ready** | Docker + Kubernetes compatible | Deploy anywhere (AWS, GCP, Railway) |

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    React 18 Frontend                      │
│         (Vite + Tailwind CSS + Framer Motion)            │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Patient Dashboard | Doctor Dashboard | Admin Dashboard  │
│  • Health Records  | • Patient List   | • User Mgmt      │
│  • Alerts         | • Risk Scores    | • Audit Logs     │
│  • Predictions    | • Reports        |                  │
└─────────────────────────────────────────────────────────┘
                           ↓ REST API
┌─────────────────────────────────────────────────────────┐
│              FastAPI Backend (Python 3.11)               │
│                                                           │
│  ├─ Auth (JWT + Bcrypt)                                 │
│  ├─ 9 REST Routers (93+ endpoints)                      │
│  ├─ Pydantic v2 Validation                              │
│  ├─ SQLAlchemy ORM                                      │
│  ├─ AI Risk Predictor (Scikit-Learn)                    │
│  ├─ Alert Service (Clinical Thresholds)                 │
│  └─ Audit Middleware (Auto-logging)                     │
└─────────────────────────────────────────────────────────┘
                           ↓ SQL
┌─────────────────────────────────────────────────────────┐
│            PostgreSQL 15 (9 Tables + Triggers)           │
│                                                           │
│  Users | Patients | Doctors | Health Records            │
│  Alerts | Predictions | Reports | Audit Logs            │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### **Backend**
```
Framework      FastAPI 0.109.2       → Async, auto-docs, production-ready
Database       PostgreSQL 15         → ACID compliance, jsonb support
ORM            SQLAlchemy 2.0        → Type-safe queries
Validation     Pydantic 2.5          → Runtime data validation
Security       JWT + Bcrypt          → Enterprise auth
ML Engine      Scikit-Learn 1.4      → Risk prediction model
```

### **Frontend**
```
Framework      React 18              → Component-based UI
Build Tool     Vite 5.0              → Lightning-fast builds
Styling        Tailwind CSS 3.4       → Utility-first CSS
Animation      Framer Motion 11       → Smooth interactions
Charting       Chart.js 4.4          → Data visualization
HTTP           Axios                 → Interceptor-based requests
```

### **DevOps**
```
Containerization  Docker              → Reproducible environments
Orchestration     Docker Compose      → Multi-container setup
CI/CD             GitHub Actions      → Automated testing & deployment
Cloud Platforms   Railway, AWS, GCP   → Scalable infrastructure
```

---

## 📊 Database Schema

```sql
── Core Tables ──
  users              (id, name, email, password_hash, role, is_active)
  patients           (patient_id, user_id, dob, gender, height, blood_group)
  doctors            (doctor_id, user_id, specialization, license_number)
  
── Clinical Data ──
  health_records     (record_id, patient_id, bp, hr, sugar, o2, temp, weight)
  alerts             (alert_id, patient_id, alert_type, severity, message)
  predictions        (prediction_id, patient_id, risk_score, risk_level)
  
── Management ──
  doctor_patient     (id, doctor_id, patient_id, is_active)  [M:M Junction]
  reports            (report_id, patient_id, doctor_id, date_from, date_to)
  
── Compliance ──
  audit_logs         (log_id, user_id, action, entity_type, ip_address)
```

---

## 🚀 Quick Start

### Prerequisites
- Docker Desktop ([download](https://www.docker.com/products/docker-desktop))
- Git
- Node.js 18+ (for local frontend dev)

### 1️⃣ Clone Repository
```bash
git clone https://github.com/Phantom-dcode/Healthgaurd-AI.git
cd Healthgaurd-AI
```

### 2️⃣ Backend Setup
```bash
cd backend
cp .env.example .env
# Edit .env → change SECRET_KEY to something unique

# Start PostgreSQL + API
docker-compose up -d
sleep 5

# Initialize database
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3️⃣ Frontend Setup (New Terminal)
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

### 4️⃣ Access the Platform
```
Frontend         → http://localhost:5173
API Swagger      → http://localhost:8000/docs
API ReDoc        → http://localhost:8000/redoc
```

### 5️⃣ Test Login
| Role | Email | Password |
|------|-------|----------|
| Admin | `admin@healthguard.ai` | `Admin@HealthGuard2024` |
| Demo Patient | Register new account | Min 8 chars, 1 Uppercase, 1 Digit |

---

## 📖 API Endpoints (93+ Endpoints)

### Authentication
```http
POST   /api/v1/auth/register        Register new user
POST   /api/v1/auth/login           Get JWT tokens
POST   /api/v1/auth/refresh         Refresh access token
POST   /api/v1/auth/logout          Logout (client-side token discard)
GET    /api/v1/auth/me              Get current user
```

### Patient Portal
```http
GET    /api/v1/patients/me          Get own profile
PUT    /api/v1/patients/me          Update profile
POST   /api/v1/health-records       Submit vitals (auto-triggers alerts + AI)
GET    /api/v1/health-records       View own history
GET    /api/v1/alerts               View personal alerts
PATCH  /api/v1/alerts/{id}          Mark alert as read/resolved
GET    /api/v1/predictions/latest   Get latest risk score
```

### Doctor Portal
```http
GET    /api/v1/doctors/me           Get profile
GET    /api/v1/doctors/my-patients  List assigned patients
POST   /api/v1/doctors/assign-patient  Assign new patient
GET    /api/v1/patients/{id}        View patient details
POST   /api/v1/reports              Generate PDF report
```

### Admin Portal
```http
GET    /api/v1/users                List all users
PATCH  /api/v1/users/{id}/deactivate  Soft-delete user
DELETE /api/v1/users/{id}           Permanently delete user
GET    /api/v1/audit-logs           View system audit trail
```

**Full API docs:** Visit `http://localhost:8000/docs` for interactive Swagger UI

---

## 🧠 AI/ML Model Details

### Risk Prediction Engine
```python
Model Type          LogisticRegression (Scikit-Learn)
Training Data       2000+ synthetic patient records
Input Features      (8 features)
├─ Age
├─ Weight (kg)
├─ Systolic BP
├─ Diastolic BP
├─ Heart Rate (bpm)
├─ Blood Sugar (mg/dL)
├─ Oxygen Level (%)
└─ Temperature (°C)

Output             Risk probability (0.0 → 1.0)
Risk Categories    
├─ Low      (0.0-0.30)    → Green
├─ Medium   (0.30-0.60)   → Amber
└─ High     (0.60-1.0)    → Red
```

### Alert Thresholds (Clinical Guidelines)
```
Blood Pressure
  ├─ Critical  systolic ≥ 180 mmHg
  ├─ High      systolic 140-179 mmHg
  └─ Low       systolic < 90 mmHg

Heart Rate
  ├─ Critical  > 150 bpm
  ├─ Elevated  100-150 bpm
  └─ Low       < 50 bpm

Blood Sugar
  ├─ Critical  > 400 mg/dL (DKA risk)
  ├─ High      200-400 mg/dL
  └─ Low       < 70 mg/dL (Hypoglycemia)

Oxygen Level
  ├─ Critical  < 90% SpO2
  └─ Low       < 95% SpO2

Temperature
  ├─ Critical  > 39.5°C
  ├─ Fever     38.0-39.5°C
  └─ Low       < 35.0°C
```

---

## 📱 User Workflows

### Patient Journey
```
Register Account → Complete Profile → Submit Daily Vitals
         ↓
AI Analyzes Vitals → Risk Score Generated
         ↓
Abnormal? → Auto Alerts Created → Alerts Dashboard
         ↓
Review Health History → Track Trends → Share with Doctor
```

### Doctor Workflow
```
Login → View Patient List → Click Patient
         ↓
See Vitals Timeline → View AI Risk Score
         ↓
Review Alerts → Generate Report → Export PDF
         ↓
Monitor Multiple Patients → Manage Assignments
```

### Admin Oversight
```
Monitor System → View All Users → Manage Accounts
         ↓
Review Audit Logs → Track User Actions
         ↓
Generate Reports → Ensure Compliance
```

---

## 🔒 Security Features

- ✅ **JWT Authentication** — Stateless, token-based auth with refresh tokens
- ✅ **Bcrypt Hashing** — Industry-standard password hashing
- ✅ **Role-Based Access Control (RBAC)** — 3 secure portals
- ✅ **Input Validation** — Pydantic v2 enforces schema at API boundary
- ✅ **SQL Injection Prevention** — SQLAlchemy parameterized queries
- ✅ **CORS Protection** — Whitelist allowed origins
- ✅ **Audit Logging** — Every action logged with user/IP/timestamp
- ✅ **Clinical Constraints** — CHECK constraints prevent bad data
- ✅ **Password Requirements** — Min 8 chars, 1 uppercase, 1 digit

---

## 📈 Project Statistics

```
Total Files       : 93
Backend Code      : 41 Python files
Frontend Code     : 35 JSX/CSS files
Database Schema   : PostgreSQL with triggers
API Endpoints     : 93+
Test Coverage     : Ready for unit tests
Code Lines        : 4000+
```

---

## 🐛 Known Limitations & Future Roadmap

### Current Limitations
- [ ] Email notifications not yet implemented (Phase 7)
- [ ] SMS alerts for critical conditions (Phase 8)
- [ ] Mobile-native app (iOS/Android) (Phase 9)
- [ ] Advanced reporting with export to Excel (Phase 9)

### Upcoming Features (Roadmap)
- **Phase 7:** Email notifications, Twilio SMS integration
- **Phase 8:** Mobile app (React Native)
- **Phase 9:** Advanced analytics, predictive alerts
- **Phase 10:** HIPAA compliance, enterprise SSO

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📝 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) file for details.

---

## 📧 Support & Contact

- **GitHub Issues:** [Report bugs or request features](https://github.com/Phantom-dcode/Healthgaurd-AI/issues)
- **Email:** blklogesh81@gmail.com
- **LinkedIn:** [Logesh Kumar](https://linkedin.com/in/logesh-kumar)
- **Portfolio:** [Phantom-dcode](https://github.com/Phantom-dcode)

---

## 👨‍💻 About the Developer

**Logesh Kumar** — B.E. CSE (AI & ML)  
KPRIET Coimbatore | Full-Stack Developer | AI/ML Enthusiast

- 🎓 Currently pursuing BTech in AI & Machine Learning
- 💼 Freelance Full-Stack Developer ([Fiverr](https://fiverr.com/logesh911))
- 🏆 GDG Hackathon Participant
- 🌍 Open-source contributor

---

## 🙏 Acknowledgments

- FastAPI for the amazing async framework
- PostgreSQL for reliable data storage
- React community for powerful UI tools
- Scikit-Learn for accessible ML
- All contributors and testers

---

<div align="center">

**Built with ❤️ using FastAPI, React, and Machine Learning**

⭐ If you found this helpful, please star the repo! ⭐

[Report Bug](https://github.com/Phantom-dcode/Healthgaurd-AI/issues) • [Request Feature](https://github.com/Phantom-dcode/Healthgaurd-AI/issues)

© 2026 Logesh Kumar. All rights reserved.

</div>
