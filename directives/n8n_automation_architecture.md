# Directive: N8N Automation Architecture (Buscador-Rate-Leads)

**ID:** DIR-005
**Status:** DRAFT
**Last Updated:** 2026-02-04

## 1. Objective
Enable fully automated and on-demand execution of the `run_pipeline.sh` lead generation system using N8N as the orchestrator and Google Sheets as the interface.

## 2. System Architecture

### 2.1 Trigger Mechanisms
The system utilizes a **Schedule-First** approach with manual override:

1.  **Automatic Trigger (Primary)**
    *   **Source:** N8N Cron/Schedule Node.
    *   **Mechanism:** Runs every Monday at 09:00 AM (configurable).
    *   **Payload:** Uses predefined query from N8N workflow variables or reads from a config file.

2.  **Manual Trigger (Secondary)**
    *   **Source:** N8N UI ("Execute Workflow" button).
    *   **Mechanism:** User manually triggers the workflow from N8N interface.
    *   **Use Case:** Ad-hoc searches or testing.

### 2.2 Execution Flow (N8N)
1.  **Input Normalization:** Define query and limit in N8N workflow variables (can be edited before manual execution).
2.  **Pipeline Execution via SSH:**
    *   **Node:** SSH (Execute Command).
    *   **Host:** `host.docker.internal` (or host machine IP).
    *   **Command:** `bash /Users/Guille/Desktop/Antigravity/01_PROJECTS/Buscador-Rate-Leads/run_pipeline.sh "{{ $json.query }}" {{ $json.limit }}`
    *   **Timeout:** 900s (15 minutes).
3.  **Result Retrieval via SSH:**
    *   **Node:** SSH (Execute Command - List Files).
    *   **Command:** `ls -t /Users/Guille/Desktop/Antigravity/01_PROJECTS/Buscador-Rate-Leads/.tmp/sheets_import_*.csv | head -n1`
    *   **Node:** SSH (Read File Content).
    *   **Command:** `cat [latest_csv_path]`
4.  **Output:**
    *   **Node:** Google Sheets (Append/Upsert).
    *   **Destination:** "Leads Database" Sheet.

## 3. Integration Standards

### 3.1 SSH Configuration (Docker to Host)
*   **SSH Key Setup:** Generate SSH key pair inside N8N Docker container and add public key to host's `~/.ssh/authorized_keys`.
*   **Host Access:** Use `host.docker.internal` (Docker Desktop) or host machine's local IP.
*   **Security:** Restrict SSH key to specific commands using `authorized_keys` restrictions (optional but recommended).
*   **Testing:** Verify connection with `ssh user@host.docker.internal whoami`.

### 3.2 Error Handling
*   If `run_pipeline.sh` returns exit code != 0:
    *   N8N catches the error.
    *   Sends an alert (Email or Telegram).
    *   Logs the error in a "Logs" sheet in the Google Spreadsheet.

## 4. Environment Requirements
*   **N8N Docker:** Must have SSH client installed (usually pre-installed in official N8N images).
*   **Host Machine:** Must have SSH server running and accessible from Docker container.
*   **Google Credentials:** N8N must have Google Drive/Sheets credentials configured (OAuth2 or Service Account).
*   **Python Environment:** Host machine must have Python3 and all dependencies installed (already configured).

---
## 5. Constraint Checklist & Confidence Score
1.  Is N8N running in Docker? (YES - confirmed by user).
2.  Is the host machine accessible via SSH from Docker? (Needs verification).
3.  Does the host have SSH server enabled? (Needs verification).
4.  Can N8N read files from host via SSH? (Needs testing).

**Confidence Score:** 4/5 (SSH setup needs verification).
