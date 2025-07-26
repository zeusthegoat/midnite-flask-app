# Project Overview
This project implements an API endpoint to monitor user deposit and withdrawal events for demo gaming site, triggering alerts for potentially unusual activity as specified in the take-home test doc

# Requirements
Python 3.7, Flask

# Setup Instructions
Open project folder in terminal

Create virtual env:
python3 -m venv venv
source venv/bin/activate

Install dependencies:
pip install -r requirements.txt

Start server (python app.py) - should start & listen on http://127.0.0.1:5000

My /event endpoint accepts JSON payloads with the expected format consisting of:
type(str): "deposit" or "withdrawal"
amount(str): Amount transacted
user_id(int): Unique user identifier
time(int): Increasing timestamp

And returns a boolean value for alerts, the designated error code if the alert value is true and the user_id. 

I've also included a /status call as a health check for the endpoint which returns a message if the server is running. 

# Example test case
curl -X POST http://127.0.0.1:5000/event \
-H "Content-Type: application/json" \
-d '{"type": "deposit", "amount": "30", "user_id": 4, "time": 1}'

curl -X POST http://127.0.0.1:5000/event \
-H "Content-Type: application/json" \
-d '{"type": "deposit", "amount": "50", "user_id": 4, "time": 2}'

curl -X POST http://127.0.0.1:5000/event \
-H "Content-Type: application/json" \
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
- The app uses in-memory storage for user histories as this is a demo project. In a production setting, I would move to persistent storage which would allow for statefulness across things like restarts.  
- Data validation checks are included; invalid/missing fields result in 400 errors.
- I added event history limiting so as to prevent user history growing indefinitely

# Updates
Added another alert function which triggers if a deposit/withdrawal pair happen with a minute of eachother