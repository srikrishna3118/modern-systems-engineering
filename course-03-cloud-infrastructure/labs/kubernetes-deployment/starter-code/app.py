"""
Simple Python Flask application for Kubernetes deployment lab.

This app serves weather data and health check endpoints.
"""

from flask import Flask, jsonify
import os
import logging
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration from environment
APP_VERSION = os.getenv("APP_VERSION", "1.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")


@app.route("/", methods=["GET"])
def index():
    """Human-facing root used by the lab's curl check."""
    return jsonify({
        "app": "weather-service",
        "status": "ok",
        "version": APP_VERSION,
    }), 200


@app.route("/health", methods=["GET"])
def health():
    """Liveness probe endpoint. Returns 200 if healthy."""
    return jsonify({"status": "healthy", "version": APP_VERSION}), 200


@app.route("/ready", methods=["GET"])
def ready():
    """Readiness probe endpoint. Returns 200 when ready to accept traffic."""
    return jsonify({"status": "ready"}), 200


@app.route("/weather", methods=["GET"])
def weather():
    """Return sample weather data."""
    return jsonify({
        "city": "San Francisco",
        "temperature": 72,
        "condition": "Sunny",
        "humidity": 60,
    }), 200


@app.route("/info", methods=["GET"])
def info():
    """Return application information."""
    return jsonify({
        "app": "weather-service",
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "timestamp": datetime.utcnow().isoformat(),
    }), 200


if __name__ == "__main__":
    logger.info(f"Starting app v{APP_VERSION} in {ENVIRONMENT} mode")
    app.run(host="0.0.0.0", port=8000, debug=False)
