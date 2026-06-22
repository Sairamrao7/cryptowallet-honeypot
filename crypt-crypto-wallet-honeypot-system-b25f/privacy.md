# Privacy & Anonymization Policy

## Purpose
This honeypot simulates a crypto wallet to study attacker behavior. It is not intended for real user interaction.

## Data Collected
- IP address (truncated for anonymization)
- User-Agent string
- Wallet credentials (hashed)
- Behavioral data (typing speed, mouse movements)

## Anonymization Measures
- **Credentials:** All credentials are hashed using SHA-256 before storage.
- **IP Address:** Only the first two octets of IPv4 addresses are stored (e.g., `192.168.x.x`).
- **User-Agent:** Stored as-is for threat intelligence.
- **Behavioral Data:** Stored for research, not linked to real identities.

## Data Usage
- Data is used for security research and threat intelligence only.
- Reports are generated in anonymized form (PDF/CSV).

## Third-Party Services
- VirusTotal and HaveIBeenPwned APIs are used for threat enrichment. Only anonymized or hashed data is sent.

## Retention & Deletion
- Data is retained for research purposes and may be deleted upon request.

## Contact
For privacy concerns, contact the system administrator.