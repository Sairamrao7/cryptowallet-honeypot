 # Crypto Wallet Honeypot - Documentation
 
 ## 1. Project Overview
 
 This project is a full-stack honeypot designed to simulate a web-based cryptocurrency wallet. Its primary purpose is to attract, deceive, and log the activities of attackers in a safe, controlled environment. By analyzing the data collected, security researchers and administrators can gain valuable insights into attacker methodologies, tools, and intentions.
 
 The system is built with a Flask backend, a simple HTML/CSS/JS frontend, and uses SQLite for lightweight, file-based logging.
 
 ---
 
 ## 2. Core Features
 
 - **Realistic Frontend:** A simple but plausible wallet interface for importing wallets, checking balances, and sending funds.
 - **Credential & Behavior Logging:** Captures not just credentials (seed phrases, private keys) but also behavioral biometrics like typing speed and mouse movements.
 - **Anonymized Data Storage:** All sensitive data is either hashed (credentials) or truncated (IP addresses) before being stored, in line with the included `privacy.md` policy.
 - **Threat Intelligence Integration (Simulated):** Includes dummy functions for integrating with threat intelligence services like VirusTotal and HaveIBeenPwned. These can be easily swapped for real API calls.
 - **Automated Reporting:** Generates on-demand PDF and Excel (`.xlsx`) reports summarizing attacker activity, perfect for both high-level briefings and deep-dive forensic analysis.
 - **SQLite Database:** All logs are stored in a single `honeypot.db` file, making the entire project highly portable and easy to inspect.
 
 ---
 
 ## 3. Project Structure
 
 The project is organized into a modular `app` package:
 
 ```
 /
 ├── app/
 │   ├── static/
 │   │   ├── style.css         # Frontend CSS
 │   │   └── app.js            # Frontend JavaScript for API calls & behavior logging
 │   ├── templates/
 │   │   └── index.html        # Main HTML file for the wallet interface
 │   ├── __init__.py           # Initializes the Flask app and database
 │   ├── models.py             # Defines the SQLAlchemy database schema (tables)
 │   ├── routes.py             # Contains all API endpoints and application logic
 │   └── main.py               # Main entry point to run the Flask server
 │
 ├── honeypot.db               # SQLite database file (created on first run)
 ├── requirements.txt          # All Python package dependencies
 ├── Documentation.md          # This file
 └── privacy.md                # Data privacy and anonymization policy
 ```
 
 ---
 
 ## 4. Setup and Installation
 
 The project is designed to run within a Python virtual environment to avoid conflicts with system-wide packages.
 
 **Prerequisites:**
 - A stable version of Python (e.g., Python 3.10, 3.11). **Python 3.12+ may cause build issues with dependencies.**
 
 **Installation Steps:**
 
 1.  **Clone the repository** (or download the source code).
 
 2.  **Open a terminal** (Command Prompt or PowerShell on Windows) in the project's root directory.
 
 3.  **Create a virtual environment:**
     ```bash
     python -m venv .venv
     ```
 
 4.  **Activate the virtual environment:**
     -   On Windows (Command Prompt): `.\.venv\Scripts\activate.bat`
     -   On Windows (PowerShell): `.\.venv\Scripts\Activate.ps1`
     -   On macOS/Linux: `source .venv/bin/activate`
 
 5.  **Install the required packages:**
     ```bash
     pip install -r requirements.txt
     ```
 
 ---
 
 ## 5. How to Run the Application
 
 With the virtual environment activated and dependencies installed:
 
 1.  Run the application from the root directory:
     ```bash
     python -m app
     ```
 
 2.  The server will start, and you will see output indicating it's running on `http://127.0.0.1:5000`.
 
 3.  Open your web browser and navigate to **http://127.0.0.1:5000** to view the honeypot wallet.
 
 ---
 
 ## 6. API Endpoints
 
 The backend exposes several API endpoints that the frontend interacts with.
 
 - `POST /import-wallet`: Logs a wallet import attempt.
   - **Body:** `{ "wallet_type": "seed|private", "credential": "..." }`
 - `GET /get-balance`: Returns a hardcoded, fake wallet balance.
 - `POST /send`: Logs an attempt to send funds.
   - **Body:** `{ "to_address": "...", "amount": 1.23, "credential": "..." }`
 - `POST /behavior-log`: Logs user behavior metrics.
   - **Body:** `{ "typing_speed": 15.4, "mouse_movements": "[...]", "session_id": "..." }`
 - `GET /report`: Generates and returns a report.
   - **Query Params:** `?format=pdf` or `?format=csv`
 
 ---
 
 ## 7. Database Schema
 
 Defined in `app/models.py`. The database consists of three tables:
 
 1.  `WalletImport`: Logs every time an attacker tries to import a wallet.
     - Fields: `id`, `timestamp`, `ip` (truncated), `user_agent`, `wallet_type`, `credential_hash` (SHA-256).
 
 2.  `SendAttempt`: Logs every time an attacker tries to send the fake funds.
     - Fields: `id`, `timestamp`, `ip`, `user_agent`, `to_address`, `amount`, `credential_hash`.
 
 3.  `BehaviorLog`: Logs behavioral data captured by the frontend JavaScript.
     - Fields: `id`, `timestamp`, `ip`, `user_agent`, `typing_speed`, `mouse_movements`, `session_id`.
 
 ---
 
 ## 8. Reporting and Analysis
 
 The reports are the core output of the honeypot. They are designed for security analysis.
 
 ### How to Generate Reports:
 - **PDF Summary:** `http://127.0.0.1:5000/report?format=pdf`
 - **Excel Deep-Dive:** `http://127.0.0.1:5000/report?format=csv`
 
 ### How to Use the Reports:
 - **The PDF** is for a high-level, visual summary. Use its graph to quickly spot spikes in activity.
 - **The Excel file** is for deep forensic investigation. Use filtering and sorting on columns like `ip` and `user_agent` to identify automated tools and persistent attackers. Correlate data between the sheets (e.g., match a `credential_hash` from an import to a send attempt) to map an attacker's complete chain of actions.
 
 This process transforms raw log data into actionable threat intelligence.