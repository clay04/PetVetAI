# app.py

from flask import Flask, request, jsonify
from controller.chatbot_controller import handle_message
from model.database import db
import config

def create_app():
    app = Flask(__name__)

    # Database config
    app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Init database
    db.init_app(app)

    # Create tables (safe for production)
    with app.app_context():
        db.create_all()

    # Webhook endpoint
    @app.route("/webhook", methods=["POST"])
    def webhook():
        data = request.get_json(silent=True) or {}

        sender = data.get("sender")
        message = data.get("message")

        # Validate input
        if not sender or not message:
            return jsonify({"error": "Invalid webhook payload"}), 400

        handle_message(sender, message)
        return jsonify({"status": "ok"})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(port=5000, debug=True)
