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
    if not RAILWAY_API_TOKEN:
        return jsonify({"error": "RAILWAY_API_TOKEN is not set"}), 400

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {RAILWAY_API_TOKEN}",
    }

    payload = {
        "query": """
            mutation DeployService($input: DeployServiceInput!) {
                deployService(input: $input) {
                    id
                    createdAt
                }
            }
        """,
        "variables": {
            "input": {
                "serviceId": SERVICE_ID
            }
        }
    }

    try:
        response = requests.post(RAILWAY_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.HTTPError as http_err:
        return jsonify({
            "error": str(http_err),
            "response": response.text
        }), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 7890))
    app.run(host="0.0.0.0", port=port)
