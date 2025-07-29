# Project Overview
This project implements an API endpoint to monitor user deposit and withdrawal events for a demo gaming site, triggering alerts for potentially unusual activity 

# Requirements
Python 3.7, Flask

# Setup Instructions
Clone the repository:
git clone https://github.com/zeusthegoat/midnite-alert-api.git
cd midnite-alert-api

Create virtual env:
python3 -m venv venv
source venv/bin/activate

Install dependencies:
pip install -r requirements.txt

Start server (python app.py) - should start & listen on http://127.0.0.1:5000

/event endpoint accepts a POST request with the following JSON structure
{
  "type": "deposit" | "withdrawal",
  "amount": "30",
  "user_id": 4,
  "time": 1
}

& returns
{
  "alert": true | false,
  "alert_code": [alert_code(s)],
  "user_id": 4
}

/status for basic health check. Returns message if server is live. 

# Alert Rules
Alerts are modularised within the alerts/ directory. The following are implemented:
- 1100 - Single withdrawal larger than £100
- 30 - Three consecutive withdrawals
- 300 - Three consecutive deposits, increasing in size
- 123 - Total withdrawals > £200 in the last 30 seconds
- 500 - Deposit & withdrawal pair within 60 seconds

# Example test case
curl -X POST http://127.0.0.1:5000/event \
-H "Content-Type: application/json" \
-H "x-api-key: zeusthegoat" \ 
-d '{"type": "deposit", "amount": "30", "user_id": 4, "time": 1}'

curl -X POST http://127.0.0.1:5000/event \
-H "Content-Type: application/json" \
-H "x-api-key: zeusthegoat" \
-d '{"type": "deposit", "amount": "50", "user_id": 4, "time": 2}'

curl -X POST http://127.0.0.1:5000/event \
-H "Content-Type: application/json" \
-H "x-api-key: zeusthegoat" \
-d '{"type": "deposit", "amount": "90", "user_id": 4, "time": 3}'

Should return the following after running the third curl statement:
{
  "alert": true,
  "alert_code": [
    300
  ],
  "user_id": 4
}

This simulates a customer making three consecutive, increasing withdrawals - results in a 300 alert being thrown

# Notes 
- Data is stored in-memory for simplicity; in production, a persistent store (e.g. Postgres) would be used.
- Type hints and error handling patterns follow basic production-ready practices.
- Designed to be easy to containerise or expand further with additional rules or database integrations.

# Updates
- Modular alert rules (each in its own file under alerts/)
- Data validation and graceful error responses
- In-memory event history capped at 10 events per user
- Logging for server and event flow visibility
- Unit test support with pytest
- Status route for health checks

# Running unit tests
Tests live in tests/ directory. Run with "pytest"
Each alert rule has its own test file and logic to ensure isolated correctness.

# Optional Frontend
Visit http://127.0.0.1:5000 to use a basic HTML tester for the /event endpoint (you must be running the server)