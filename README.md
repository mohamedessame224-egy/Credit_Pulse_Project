# Credit Pulse — منصة استبيانات قطاع الائتمان
### البنك الأهلي المصري | National Bank of Egypt

---

## 🚀 Quick Start — البدء السريع

### Windows
```
Double-click:  run_project.bat
```

### Mac / Linux
```bash
python run.py
```

Then open your browser at: **http://127.0.0.1:5000**

---

## 📋 Step 1 — Install Requirements

Open a terminal (Command Prompt / PowerShell) inside the project folder:

```bash
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- Flask-SQLAlchemy (database)
- Flask-Login (admin authentication)
- pandas, openpyxl (Excel reports)
- reportlab (PDF reports)
- python-docx (Word reports)

---

## ▶️ Step 2 — Run the Project

### Option A — Double-click (Windows)
```
run_project.bat
```

### Option B — Python command
```bash
python run.py
```

The app will:
1. Initialize the database automatically
2. Create default admin account
3. Seed 10 departments
4. Create a sample survey with 4 sections & 11 questions
5. Open your browser automatically at http://127.0.0.1:5000

---

## 🌐 Step 3 — Access the Application

| URL | Description |
|-----|-------------|
| http://127.0.0.1:5000 | Employee Survey Portal |
| http://127.0.0.1:5000/admin | Admin Dashboard |
| http://127.0.0.1:5000/admin/login | Admin Login |

---

## 🔐 Admin Login

| Field | Value |
|-------|-------|
| Username | `admin` |
| Password | `CreditPulse2024` |

> ⚠️ Change the password in production by modifying `utils/init_db.py`

---

## 📊 Admin Dashboard Features

### Overview Dashboard
- Total participants counter
- Participating departments count
- Average satisfaction score
- Credit Pulse Score (0–100%)
- Anonymous responses count
- 14-day participation trend chart
- Department comparison bar chart
- Rating questions analysis

### Responses Page
- Full table of all responses
- Filter by department / search / anonymous type
- Click "View" to see full response details in a modal

### Survey Manager
- View survey structure: sections, questions, types, answer counts
- Instructions for adding new surveys

### Reports
| Format | Contents |
|--------|----------|
| Excel  | Summary sheet + Raw responses + Department analysis |
| PDF    | Cover + Executive summary + Department table |
| Word   | Formatted management report |

---

## 🌍 Language Switching

Click the language button in the top bar:
- **عربي → English** switches to English (LTR layout)
- **English → العربية** switches to Arabic (RTL layout)

All pages, labels, reports, and charts switch language dynamically.

---

## ➕ How to Add a New Survey

### Method 1 — Edit init_db.py
1. Open `utils/init_db.py`
2. Find the survey creation block
3. Add new sections and questions following the existing pattern
4. Delete the database file: `instance/credit_pulse.db`
5. Restart the app — it will recreate everything

### Method 2 — Use the TXT Template
See `data/sample_survey.txt` for the format. Future versions will import directly.

### Question Types Supported
| Type | Description |
|------|-------------|
| `rating` | Star/number scale 1–5 |
| `single_choice` | Radio buttons |
| `multiple_choice` | Checkboxes |
| `text` | Free-text comment box |

---

## 🎭 Load Demo Data

To populate the dashboard with realistic test data:

```bash
python utils/seed_demo.py
```

This adds ~50–80 sample responses across all departments.

---

## 📁 Project Structure

```
Credit_Pulse_Project/
├── run.py                  ← Main entry point
├── run_project.bat         ← Windows double-click launcher
├── app.py                  ← Flask application factory
├── requirements.txt        ← Python packages
│
├── models/
│   └── models.py           ← Database models
│
├── routes/
│   ├── employee.py         ← Employee portal routes
│   ├── admin.py            ← Admin dashboard routes
│   └── reports.py          ← Excel / PDF / Word generation
│
├── utils/
│   ├── init_db.py          ← Database initialization & seeding
│   ├── seed_demo.py        ← Demo data generator
│   └── translations.py     ← Arabic / English translation strings
│
├── templates/
│   ├── base.html           ← Master layout
│   ├── employee/
│   │   ├── welcome.html    ← Landing page
│   │   ├── info.html       ← Employee info form
│   │   ├── survey.html     ← Survey questions
│   │   └── thanks.html     ← Confirmation page
│   └── admin/
│       ├── base_admin.html ← Admin sidebar layout
│       ├── login.html      ← Admin login
│       ├── dashboard.html  ← Analytics dashboard
│       ├── responses.html  ← Response table
│       └── survey_manager.html ← Survey structure
│
├── static/
│   └── css/
│       └── main.css        ← NBE-inspired stylesheet
│
├── data/
│   └── sample_survey.txt   ← Survey template file
│
├── reports/                ← Generated reports saved here
└── instance/
    └── credit_pulse.db     ← SQLite database (auto-created)
```

---

## 🛠️ Troubleshooting

**Port already in use:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <pid> /F

# Mac/Linux
kill -9 $(lsof -ti:5000)
```

**Module not found:**
```bash
pip install -r requirements.txt --upgrade
```

**Database issues:**
```bash
# Delete and recreate
del instance\credit_pulse.db   # Windows
rm instance/credit_pulse.db    # Mac/Linux
python run.py
```

**Arabic text in PDF not rendering correctly:**
The PDF report uses standard Latin fonts. For full Arabic shaping in PDF, install `arabic-reshaper` and `python-bidi` (already in requirements.txt).

---

## 🔮 Future Roadmap

- [ ] AI-powered comment sentiment analysis
- [ ] Historical trend comparison across survey cycles
- [ ] Multiple concurrent surveys
- [ ] Role-based access (viewer / analyst / admin)
- [ ] Email notifications for new submissions
- [ ] Excel import for survey questions
- [ ] Heat map visualization by department
- [ ] Action tracking and follow-up module
- [ ] PostgreSQL migration for production

---

## 🏦 Branding

Credit Pulse uses the official NBE corporate color palette:

| Color | Hex | Usage |
|-------|-----|-------|
| Navy | `#1B3A6B` | Primary brand color, headers, nav |
| Dark Navy | `#0F2347` | Top bar, footer, sidebar |
| Gold | `#C8A951` | Accents, highlights, CTA buttons |
| Light Gold | `#DFC06A` | Hover states |
| Red | `#C41230` | Alerts, required fields |

Typography: **Cairo** (Arabic), **Inter** (English)

---

*Credit Pulse © 2024 — National Bank of Egypt, Credit Sector*
*For internal use only — جميع الحقوق محفوظة للبنك الأهلي المصري*
