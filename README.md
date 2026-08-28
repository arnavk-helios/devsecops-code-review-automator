# DevSecOps Code Review Automator
**Multi-Agent LLM Architecture integrating Gemini & Claude**

**Prepared by:** Arnav Kshirsagar ([@arnavk-helios](https://github.com/arnavk-helios))  
**Live Command Center:** [devsecops-code-review-automator.vercel.app](https://devsecops-code-review-automator.vercel.app)

---

## Project Goal
A multi-agent AI pipeline that intercepts GitHub Pull Requests, performs Static Application Security Testing (SAST), coordinates specialized LLM agent reviews, alerts engineering channels, and records execution audit trails[cite: 1, 2, 4].

---

## Tech Stack
* **Languages & Frameworks:** Python (FastAPI), TypeScript (Next.js), Bash, SQL
* **AI & Multi-Agent:** Google Gemini 3.6 Flash (AppSec Scanner & Architect Engine)
* **Security & Tooling:** Bandit (SAST), GitHub REST API, SQLite3
* **Alerts & Deployment:** Discord Webhooks, ngrok, Vercel

---

## Architecture Overview

```text
[ GitHub Pull Request Event ]
              │
              ▼
   [ FastAPI Webhook Server ]
              │
      ┌───────┴───────────────────────┐
      ▼                               ▼
[ Bandit SAST Scan ]          [ GitHub API Diff Fetch ]
      │                               │
      └───────┬───────────────────────┘
              ▼
  [ Agent 1: AppSec Scanner (Gemini) ] ──▶ (JSON Vulnerability Report)
              │
              ▼
  [ Agent 2: Senior Architect (Gemini) ] ──▶ (Markdown Engineering Review)
              │
      ┌───────┴───────────────────────┬────────────────────────┐
      ▼                               ▼                        ▼
[ GitHub PR Comment ]       [ Discord Alert Ping ]   [ SQLite Audit Log ]
                                                               │
                                                               ▼
                                                  [ Next.js Vercel Dashboard ]
