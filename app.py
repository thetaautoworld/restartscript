import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

RAILWAY_API_URL = "https://backboard.railway.app/graphql/v2"
RAILWAY_API_TOKEN = os.getenv("RAILWAY_API_TOKEN")
DEPLOYMENT_ID = os.getenv("DEPLOYMENT_ID")

@app.route("/restart", methods=["GET"])
def restart_deployment():
    if not DEPLOYMENT_ID:
        return jsonify({"error": "DEPLOYMENT_ID is not set"}), 400

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {RAILWAY_API_TOKEN}",
    }

    query = {
        "query": f"""
        mutation {{
            deploymentRestart(id: "{DEPLOYMENT_ID}")
        }}
        """
    }

    try:
        response = requests.post(RAILWAY_API_URL, headers=headers, json=query)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 7890))
    app.run(host="0.0.0.0", port=port)