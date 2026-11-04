"""
Weather service used by the Kubernetes lab (solution).

The same process runs under Docker Compose for a local check and under
the manifests in k8s/ when a cluster is available.
"""

from flask import Flask, jsonify
import os
import logging
from datetime import datetime, timezone

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

APP_VERSION = os.getenv("APP_VERSION", "1.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "app": "weather-service",
        "status": "ok",
        "version": APP_VERSION,
    }), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "version": APP_VERSION}), 200


@app.route("/ready", methods=["GET"])
def ready():
    return jsonify({"status": "ready"}), 200


@app.route("/weather", methods=["GET"])
def weather():
    return jsonify({
        "city": "San Francisco",
        "temperature": 72,
        "condition": "Sunny",
        "humidity": 60,
    }), 200


@app.route("/info", methods=["GET"])
def info():
    return jsonify({
        "app": "weather-service",
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }), 200


if __name__ == "__main__":
    logger.info("Starting app v%s in %s mode", APP_VERSION, ENVIRONMENT)
    app.run(host="0.0.0.0", port=8000, debug=False)
