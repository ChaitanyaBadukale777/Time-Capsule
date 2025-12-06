# backend/app.py

from flask import Flask, jsonify
from flask_cors import CORS
from controllers.capsule_controller import capsule_bp

def create_app():
    app = Flask(__name__)
    CORS(app)  # allow frontend to call backend

    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"}), 200

    app.register_blueprint(capsule_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
