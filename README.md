# FinPlot AI — AI-Powered Bookkeeping & Financial Reconciliation System

**FinPlot AI** is an intelligent accounting automation platform inspired by modern AI-native financial software (such as Rillet). Designed specifically for small businesses, agencies, and freelancers, FinPlot AI streamlines ledger management, automated bank statement ingestion, financial health analytics, and deterministic cash flow tracking.

> **Project Phase:** Currently in **Phase 1: Working Dashboard & Transaction Management**.  
> Features for future phases (Supabase Auth sessions, Gemini Assistant, Invoice OCR & Automated Reconciliation) are architected with clean extension points and will be implemented incrementally.

---

## 🏛️ System Architecture

FinPlot AI is built with a decoupled 3-tier architecture:

```
┌────────────────────────────────────────────────────────┐
│            Streamlit Modern Web Presentation           │
│  (Inter Typography, Glassmorphism Cards, Dark Palette) │
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│                 Services & Logic Layer                 │
│  ├── TransactionService (CRUD Orchestration)           │
│  ├── AnalyticsService (Deterministic Calculations)     │
│  └── ImportService (CSV/Excel Ingestion & Duplicates)  │
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│                 Data Repository Layer                  │
│  ├── Supabase PostgreSQL (Cloud Persistent with RLS)   │
│  └── SQLite Fallback Engine (Local Persistent Mode)     │
└────────────────────────────────────────────────────────┘
```

---

## 🚀 Key Features in Phase 1

1. **Executive Financial Dashboard**
   - Real-time summary KPI cards: **Total Income**, **Total Expenses**, and **Net Cash Flow** with margin status badges.
   - Interactive Plotly figures:
     - Grouped Monthly Income vs. Expense comparison with net trendline.
     - Expense distribution breakdown by category (Interactive Donut chart).
     - Running cumulative cash balance trajectory over time.
   - Filterable date window (e.g., Last 30, 90, 180 days, or custom).

2. **Complete Transaction Management (CRUD)**
   - **Create**: Add transactions with real-time validation (strictly positive amounts, validated date, canonical/custom categories).
   - **Read**: Full-text search (payee, memo, category, payment mode) and multi-facet filtering.
   - **Update**: In-place edit drawer pre-populated with transaction data.
   - **Delete**: Protected deletion flow with mandatory two-step confirmation.

3. **Isolated Demonstration Dataset**
   - Explicit **"Load Demo"** action seeds 19 realistic, multi-month business transactions tagged with `is_demo = true`.
   - Explicit **"Clear Demo"** action safely purges sample records without touching live financial data.
   - Database telemetry panel displays real vs. demo record breakdown.

4. **Robust CSV / Excel Statement Ingestion**
   - Upload `.csv`, `.xlsx`, or `.xls` bank and accounting statements.
   - Automated column alias detection (`Date`, `Memo`, `Total`, `Direction`, etc.).
   - Pre-import validation preview showing **Valid Rows**, **Detected Duplicates**, and **Invalid Rows**.
   - Duplicate prevention prevents redundant entries matching existing transactions.
   - Downloadable CSV template for instant compliance.

5. **Dual Storage Engine (No Fabricated Sync)**
   - Direct integration with **Supabase PostgreSQL** via official SDK and Row-Level Security (RLS).
   - Graceful fallback to **Local SQLite Engine** (`finplot_local.db`) when cloud credentials are not supplied.
   - Transparent UI indicator notifies the user whether they are running in **Supabase Cloud Active** or **Local SQLite Demo Mode**.

---

## 📁 Repository Structure

```
FinPlot/
├── app.py                      # Main Streamlit application entry point
├── .env.example                # Template for environment variables
├── .gitignore                  # Git ignore rules for venv, secrets, and caches
├── requirements.txt            # Python dependencies
├── README.md                   # Complete architectural and setup guide
│
├── components/                 # Modular Streamlit UI presentation components
│   ├── __init__.py
│   ├── styles.py               # Custom CSS design system (Inter typography, cards, badges)
│   ├── cards.py                # Metric KPI summary cards
│   ├── charts.py               # Plotly interactive financial visualizations
│   ├── transaction_form.py     # Add/Edit transaction form with validation
│   └── transaction_table.py    # Searchable transaction table with confirmation dialogs
│
├── database/                   # Persistent data access layer
│   ├── __init__.py
│   ├── connection.py           # Supabase client manager & environment checking
│   └── repository.py           # Unified repository (Supabase Cloud + SQLite fallback)
│
├── services/                   # Core business logic and analytics services
│   ├── __init__.py
│   ├── analytics_service.py    # Deterministic formulas for income, expense, net cash flow
│   ├── transaction_service.py  # Business logic & repository orchestration
│   └── import_service.py       # Statement parsing, validation & duplicate detection
│
├── utils/                      # Input validators and sample data
│   ├── __init__.py
│   ├── validators.py           # Strict payload validation & type parsing
│   └── sample_data.py          # Curated multi-month sample transactions
│
├── supabase/
│   └── migrations/
│       └── 20260101_init_schema.sql  # Database schema, triggers, indexes, and RLS policies
│
└── tests/                      # Automated test suite (Pytest)
    ├── __init__.py
    ├── test_calculations.py    # Financial calculations and analytics tests
    ├── test_validation.py      # Input validation & amount parsing tests
    ├── test_import.py          # CSV import, mapping & duplicate detection tests
    └── test_repository.py      # Data repository and CRUD integration tests
```

---

## 🛠️ Windows Setup & Installation Guide

### Prerequisites
- **Python 3.10+** (Tested on Python 3.14 on Windows 11/10)
- **Git** (optional, for version control)

### Step 1: Open PowerShell in Project Directory
Open **PowerShell** or **Command Prompt** and navigate to the project directory:
```powershell
cd C:\Users\vdiwa\OneDrive\文档\Desktop\FinPlot
```

### Step 2: Create a Virtual Environment
```powershell
python -m venv .venv
```

### Step 3: Activate the Virtual Environment
- **PowerShell:**
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
  *(If you get a script execution policy error in PowerShell, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` once).*
- **Command Prompt (CMD):**
  ```cmd
  .\.venv\Scripts\activate.bat
  ```

### Step 4: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 5: Configure Environment Variables
Copy `.env.example` to `.env`:
```powershell
Copy-Item .env.example .env
```

Open `.env` in your text editor:
```env
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_KEY=your-supabase-anon-key-here
APP_ENV=development
```

> **Note on Local Demo Mode:** If you do not yet have a Supabase project, you can leave `.env` as is! FinPlot AI will automatically run in **Local SQLite Demo Mode** with persistent storage in `finplot_local.db`. You can connect Supabase at any time.

---

## 🗄️ Supabase Database Setup & RLS Migration

To connect FinPlot AI to Supabase Cloud:

1. **Create a Free Project**: Sign in to [Supabase](https://supabase.com) and create a new project.
2. **Execute SQL Migration**:
   - In your Supabase dashboard, click **SQL Editor** from the left navigation.
   - Click **New Query**.
   - Copy the entire contents of [`supabase/migrations/20260101_init_schema.sql`](supabase/migrations/20260101_init_schema.sql).
   - Paste into the SQL editor and click **Run**.
3. **Verify Created Objects**:
   - Table `public.transactions` with columns: `id`, `user_id`, `transaction_date`, `description`, `amount`, `transaction_type`, `category`, `payment_method`, `notes`, `is_demo`, `created_at`, `updated_at`.
   - Indexing on `user_id`, `transaction_date`, `category`, `is_demo`.
   - Row-Level Security (RLS) policies protecting user data access.
4. **Copy API Keys**:
   - Go to **Project Settings** -> **API**.
   - Copy `Project URL` and `anon public` key into your `.env` file.

---

## 🏃 Running the Application

With your virtual environment activated, run:

```powershell
streamlit run app.py
```

The application will launch in your default web browser at `http://localhost:8501`.

---

## 🧪 Running Automated Tests

Run the full test suite with `pytest`:

```powershell
pytest -v
```

All 23 tests covering financial calculations, transaction validation, CSV statement parsing, duplicate detection, and repository CRUD will execute.

```
tests/test_calculations.py::test_calculate_metrics_empty PASSED
tests/test_calculations.py::test_calculate_metrics_surplus PASSED
tests/test_calculations.py::test_calculate_metrics_deficit PASSED
tests/test_calculations.py::test_monthly_summary_aggregation PASSED
tests/test_calculations.py::test_category_summary PASSED
tests/test_calculations.py::test_cumulative_cashflow_trend PASSED
tests/test_import.py::test_template_generation PASSED
tests/test_import.py::test_column_mapping_aliases PASSED
tests/test_import.py::test_column_mapping_missing_required PASSED
tests/test_import.py::test_parse_and_validate_file_valid_csv PASSED
tests/test_import.py::test_parse_and_validate_file_invalid_rows PASSED
tests/test_import.py::test_duplicate_detection_against_db PASSED
tests/test_repository.py::test_create_and_get_transaction PASSED
tests/test_repository.py::test_update_transaction PASSED
tests/test_repository.py::test_delete_transaction PASSED
tests/test_repository.py::test_demo_data_isolation_and_clear PASSED
tests/test_validation.py::test_parse_amount_valid PASSED
tests/test_validation.py::test_parse_amount_invalid PASSED
tests/test_validation.py::test_parse_date_formats PASSED
tests/test_validation.py::test_parse_date_invalid PASSED
tests/test_validation.py::test_validate_transaction_payload_valid PASSED
tests/test_validation.py::test_validate_transaction_payload_negative_amount PASSED
tests/test_validation.py::test_validate_transaction_payload_missing_required PASSED
============================= 23 passed in 1.29s ==============================
```

---

## ⚠️ Known Limitations & Assumptions (Phase 1)

1. **Authentication:** Phase 1 focuses on full CRUD and financial analytics. Transactions in demo mode operate with `user_id = NULL` and `is_demo = true`. Full sign-up/sign-in flows with Supabase Auth will be activated in Phase 2.
2. **AI & Reconciliation:** AI chat assistance (Gemini API) and automated invoice reconciliation (OCR + matching rules) will be introduced in Phases 3 and 4 respectively.
3. **Currency Support:** Monetary values are modeled in USD with standard two-decimal precision. Multi-currency foreign exchange conversion is outside the educational scope of Phase 1.

---

## 🔮 Project Roadmap

- [x] **Phase 1: Working Dashboard & Transaction Management** (Completed)
- [ ] **Phase 2: Authentication & Data Import Enhancements** (Supabase Auth sessions, multi-tenant user isolation)
- [ ] **Phase 3: Gemini AI Financial Assistant** (Natural language Q&A, server-side aggregations, category recommendations)
- [ ] **Phase 4: Smart Vendor Rules & Invoice Reconciliation** (Deterministic matching rules, PDF OCR extraction)
- [ ] **Phase 5: Financial Reporting, Testing & Cloud Deployment** (P&L statements, balance sheet projections, production hardening)
