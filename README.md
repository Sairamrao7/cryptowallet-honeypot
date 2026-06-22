# cryptowallet-honeypot
# Crypto Wallet Honeypot

A full-stack honeypot simulating a crypto wallet (Flask backend, HTML/CSS/JS frontend).

## Features
- Import wallet (seed/private key)
- Fake balance
- Simulated send coins
- SQLite logging (IP, user-agent, credentials, behavioral data)
- VirusTotal & HaveIBeenPwned API integration (dummy fallback)
- User behavior capture (typing speed, mouse movements)
- PDF/CSV threat reports with graphs
- Anonymization: hashed credentials, truncated IPs

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   python -m app
   ```
3. Open your browser at [http://localhost:5000](http://localhost:5000)

## Privacy
See [privacy.md](privacy.md).
# cryptowallet-honeypot
