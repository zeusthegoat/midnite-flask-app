from flask import Flask, request, jsonify, render_template
from alerts import check_alerts
from auth import check_api_key
from logger import setup_logger
logger = setup_logger("midnite-api")

app = Flask(__name__)
user_history = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/status", methods=["GET"])
def status():
    return {
        "status": "ok",
        "message": "Midnite alert API is running"
    }, 200

@app.route("/event", methods=["post"])
def handle_event():
    logger.info("Receivend /event request")

    auth_error = check_api_key()
    if auth_error:
        logger.warning("Authentication failed")
        return auth_error

    data = request.get_json()
    logger.info("Payload received: :s", data)
    
    if not data:
        logger.error("Invalid JSON payload")
        return jsonify({"error": "Invalid JSON payload"}), 400
    
    user_id = data.get("user_id")
    if user_id is None:
        logger.error("Missing user_id in payload")
        return jsonify({"error": "Missing user_id"}), 400
    
    if user_id not in user_history:
        logger.info("New user_id detected: %s", user_id)
        user_history[user_id] = []

    user_history[user_id].append(data)
    user_history[user_id] = user_history[user_id][-10:]
    logger.debug("Updated user history for %s: %s", user_id, user_history[user_id])

    try:
        alert, alert_code = check_alerts(user_history[user_id])
        logger.info("Alert check complete for %s - Alert: %s, Codes: %s", user_id, alert, alert_code)

        return jsonify({
            "alert": alert,
            "alert_code": alert_code,
            "user_id": user_id
        })
    except Exception as e:
        logger.exception("Error during alert check for user %s: %s", user_id, str(e))
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    print("Starting flask app...")
    app.run(debug=True)