from flask import Flask, request, jsonify, render_template, Response
from alerts import check_alerts
from auth import check_api_key
from prometheus_flask_exporter import PrometheusMetrics
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session as SessionType
from sqlalchemy import create_engine
from models import Event, Base
from logger import setup_logger
logger = setup_logger("midnite-api")

app = Flask(__name__)
DATABASE_URL = "postgresql://midnite_user:midnite_pass@db:5432/midnite"

engine = create_engine(DATABASE_URL)
# Base.metadata.create_all(engine) #
Session = sessionmaker(bind=engine)

metrics = PrometheusMetrics(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/status", methods=["GET"])
def status():
    return {
        "status": "ok",
        "message": "Midnite alert API is running"
    }, 200

@app.route("/event", methods=["POST"])
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
    
    # Save event to DB
    try:
        with Session() as session:   # Using context manager to prevent session issues
            event = Event(
                user_id=user_id,
                event_type=data["type"],
                amount=float(data["amount"]),
                timestamp=int(data["time"])
        )
        session.add(event)
        session.commit()

        # Fetching latest 10 events for this user
        recent_events = (
            session.query(Event)
            .filter_by(user_id=user_id)
            .order_by(Event.timestamp.desc())
            .limit(10)
            .all()
        )

        # Converting to list of dicts for alert logic
        event_history = [
            {
                "user_id": e.user_id,
                "type": e.event_type,
                "amount": str(e.amount),
                "time": e.timestamp
            }
            for e in reversed(recent_events)  # Reversed to get chronological order
        ]

        alert, alert_code = check_alerts(event_history)

        return jsonify({
            "alert": alert,
            "alert_code": alert_code,
            "user_id": user_id
        })

    except OperationalError:
        logger.error("Database connection error")
        return jsonify({"error": "Database is unavailable"}), 503
    except Exception as e:
        logger.exception("Error during DB operation or alert check: %s", str(e))
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    print("Starting flask app...")
    app.run(host="0.0.0.0", port=5000, debug=True)