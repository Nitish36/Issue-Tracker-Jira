# Issue-Tracker-Jira

Designed and implemented a cross-platform governance automation framework integrating Jira, Smartsheet Control Center, and Looker dashboards.

### 📌 Overview
This project is an automated governance and reporting framework that integrates:
  1) Jira Issue Tracking
  2) Smartsheet (Control Center project provisioning)
  3) Google Sheets data aggregation
  4) Looker Studio dashboards

It ensures structured project creation, centralized tracking, and real-time reporting across systems.

### 🏗 Architecture Flow
Jira → Smartsheet (Control Center Projects) → Google Sheets → Looker Dashboard

### Workflow:
  1) Issues are created and updated in Jira.
  2) Smartsheet Control Center provisions structured project templates.
  3) Users fill project-level details inside Smartsheet.
  4) Python automation extracts and transforms relevant data.
  5) Data is pushed to Google Sheets.
  6) Looker Studio reads from Google Sheets to power live dashboards.

### ⚙️ Key Features
  1) 🔄 Automated Jira API data extraction
  2) 📊 Structured Smartsheet project governance
  3) 🔐 Secure API authentication using GitHub Secrets
  4) 🧮 Data transformation & normalization
  5) 📤 Automated push to Google Sheets
  6) 📈 Live dashboard integration (Looker Studio)
  7) 🚀 CI/CD execution using GitHub Actions

### 🔐 Security & Configuration
Sensitive credentials are stored securely using GitHub Actions secrets:
  1) JIRA_SECRET
  2) GSHEET_SECRET
No credentials are hardcoded in the repository.

### 🧠 Business Impact
  1) Improves visibility across projects
  2) Reduces manual tracking
  3) Enhances governance and auditability
  4) Enables real-time executive reporting
  5) Bridges operational systems with analytics

### 🛠 Tech Stack
  1) Python
  2) Jira REST API
  3) Smartsheet API
  4) Google Sheets API
  5) GitHub Actions
  6) Looker Studio

### 📊 Example Use Cases
  1) Project variance monitoring
  2) Resource planning insights
  3) Governance compliance checks
  4) Cross-platform project lifecycle tracking
