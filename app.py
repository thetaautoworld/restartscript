import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

RAILWAY_API_URL = "https://backboard.railway.app/graphql/v2"
RAILWAY_API_TOKEN = os.getenv("RAILWAY_API_TOKEN")
SERVICE_ID = os.getenv("SERVICE_ID")

@app.route("/restart", methods=["GET"])
def restart_service():
    if not SERVICE_ID:
        return jsonify({"error": "SERVICE_ID is not set"}), 400

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {RAILWAY_API_TOKEN}",
    }

    query = {
        "query": f"""
        mutation {{
            deployService(input: {{
                serviceId: "{SERVICE_ID}"
            }}) {{
                id
            }}
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
