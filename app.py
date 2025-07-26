from flask import Flask, request, jsonify, render_template
from alerts import check_alerts
from auth import check_api_key

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
    auth_error = check_api_key()
    if auth_error:
        return auth_error

    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400
    
    user_id = data.get("user_id")
    if user_id is None:
        return jsonify({"error": "Missing user_id"}), 400
    
    if user_id not in user_history:
        user_history[user_id] = []

    user_history[user_id].append(data)
    user_history[user_id] = user_history[user_id][-10:]

    alert, alert_code = check_alerts(user_history[user_id])

    return jsonify({
        "alert": alert,
        "alert_code": alert_code,
        "user_id": user_id
    })

if __name__ == "__main__":
    print("Starting flask app...")
    app.run(debug=True)