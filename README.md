# 🎯 The David Protocol

> **Eradicating the "Credit Invisible" Penalty through AI-Driven Cash-Flow Underwriting.**

Traditional credit bureaus penalize millions of financially responsible individuals simply for lacking a history of debt. These credit invisible consumers, including students and gig workers, are unfairly denied essential loans despite maintaining consistent, positive cash flow, creating a harsh cycle of systemic financial exclusion.

**The David Protocol** securely ingests read-only bank data via the Plaid API. We leverage Gemini's NLP to accurately categorize messy spending habits instantly. Finally, our deterministic machine learning model evaluates cash-flow stability, generating a fair, fully auditable Financial Resilience Score to safely unlock essential credit for millions of untraditional borrowers.

---

## ⚙️ Tech Stack

**Frontend (User Interface & Dashboard)**
* **Framework:** [Next.js](https://nextjs.org/) (App Router)
* **Styling:** Tailwind CSS + [Tremor](https://www.tremor.so/) (Financial UI Components)
* **Integration:** `react-plaid-link`

**Backend (API & Data Orchestration)**
* **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python)
* **Server:** Uvicorn
* **Database:** PostgreSQL (Hosted via Supabase/Neon)
* **ORM:** SQLModel / SQLAlchemy

**Artificial Intelligence & Machine Learning**
* **NLP Categorization:** [Google Gemini API](https://ai.google.dev/) (Strict JSON Schema outputs)
* **Risk Engine:** Scikit-Learn / XGBoost (Deterministic Classification)

**External APIs**
* **Financial Data:** [Plaid API](https://plaid.com/) (Sandbox Environment)

---

## 🧠 How It Works (The Pipeline)

1. **Secure Authentication:** Users link their bank accounts via the Plaid Link modal (Zero credentials stored on our servers).
2. **Data Ingestion:** The FastAPI backend fetches up to 90 days of raw transaction history.
3. **AI Cleaning (The Smart Layer):** Raw, messy transaction strings (e.g., `ACH*T-MOBILE WEB PYMT XXXXX992`) are batched and sent to the Gemini API, which categorizes them strictly into `Rent`, `Utilities`, `Income`, or `Discretionary`.
4. **Deterministic Scoring (The Safe Layer):** The categorized data is evaluated by our XGBoost model against key features (e.g., Income-to-Rent ratio, utility payment consistency) to generate a **Financial Resilience Score (1-100)**.
5. **Real-Time Dashboard:** The user's score and categorized spending habits are visualized instantly on the Next.js/Tremor frontend.

---

## 💻 Local Development Setup

### Prerequisites
* Node.js (v18+)
* Python (3.10+)
* API Keys: Plaid (Sandbox), Google Gemini
* PostgreSQL Database URL (Supabase or Neon)

### 1. Backend Setup (FastAPI)
Navigate to the backend directory and set up your Python environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
