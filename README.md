# DevSecOps Code Review Automator
**Multi-Agent LLM Architecture integrating Gemini & Claude**

**Prepared for:** Arnav Kshirsagar | **GitHub:** [@arnavk-helios](https://github.com/arnavk-helios)

---

## Project Goal
Build a scalable, multi-agent AI workflow that intercepts GitHub pull requests, performs deep static application security testing (SAST), and drafts architectural reviews[cite: 2]. This project demonstrates applied cybersecurity, orchestration, and full-stack development to prospective engineering teams[cite: 2].

---

## Tech Stack
* **Languages & Scripts:** Python, Bash, SQL[cite: 2]
* **AI & Orchestration:** LangChain, Google Gemini, Anthropic Claude 3.5 Sonnet[cite: 2]
* **Security & Tooling:** Bandit (SAST), GitHub REST API, SQLite[cite: 2]
* **Webhooks & Frontend (Planned):** FastAPI/Flask, Next.js, Vercel[cite: 2]

---

## System Architecture & Roadmap

### ✅ Phase 1: Environment Setup & Foundation (Backend)
* **Isolated Environment:** Configured a Python virtual environment (`devsecops-env`) on macOS[cite: 1, 2].
* **Core SDKs:** Installed `langchain-core`, `google-genai`, and `anthropic` for model communication and routing[cite: 1, 2].
* **Audit Database:** Initialized a local SQLite database (`audit_logs.db`) to log pull request scans, security flags, and agent decisions[cite: 1, 2].

### ✅ Phase 2: Forging the "Skills" (Security Tooling)
* **`Fetch_Diff` Skill:** Python function using the GitHub REST API to extract raw code changes from pull requests[cite: 2].
* **`Security_Scan` Skill:** Linux Bash script (`run_sast.sh`) wrapping Bandit to generate JSON security reports, executed via a Python wrapper[cite: 2].
* **`Query_History` Skill:** Formulated SQL queries to retrieve past audit logs from SQLite for coding standard consistency[cite: 2].

### 🚧 Phase 3: The Brains (Multi-Agent Orchestration)
* **Agent 1 - Security Scanner (Gemini):** Instructed as an AppSec engineer to identify vulnerabilities (hardcoded secrets, SQL injection) and output structured JSON[cite: 2].
* **Agent 2 - Architect (Claude):** Instructed as a Senior Staff Engineer to draft a comprehensive architectural review from the diff and security report[cite: 2].
* **Handoff Protocol:** Deterministic Python routing logic to ensure Gemini's scan completes before Claude begins[cite: 2].

### ⏳ Phase 4: The Connectors (Real-World Integration)
* **Input Webhook:** Local FastAPI/Flask server listening for GitHub `pull_request` opened events[cite: 2].
* **Output Commenter:** Automated GitHub API commenter to publish final reviews directly to PR threads[cite: 2].
* **Alerting System:** Discord/Slack webhook integration to broadcast scan summary alerts[cite: 2].

### ⏳ Phase 5: The Command Center (Frontend Dashboard)
* **Dashboard:** Next.js application hosted on Vercel to display real-time execution logs and audit history[cite: 2].

---

## Quick Start (Local Setup)

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/arnavk-helios/devsecops-code-review-automator.git](https://github.com/arnavk-helios/devsecops-code-review-automator.git)
   cd devsecops-code-review-automator
