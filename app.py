import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

URL = "https://backboard.railway.app/graphql/v2"
TOKEN = os.getenv("RAILWAY_API_TOKEN")
SERVICE_ID = os.getenv("SERVICE_ID")
ENV_ID = os.getenv("ENVIRONMENT_ID")

@app.route("/restart", methods=["GET"])
def restart():
    if not all([TOKEN, SERVICE_ID, ENV_ID]):
        return jsonify({"error": "Missing SERVICE_ID or ENVIRONMENT_ID or token"}), 400

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {TOKEN}"}
    payload = {
        "query": """
        mutation serviceInstanceRedeploy($environmentId: String!, $serviceId: String!) {
          serviceInstanceRedeploy(environmentId: $environmentId, serviceId: $serviceId)
        }
        """,
        "variables": {"environmentId": ENV_ID, "serviceId": SERVICE_ID}
    }

    try:
        resp = requests.post(URL, json=payload, headers=headers)
        resp.raise_for_status()
        return jsonify(resp.json())
    except requests.HTTPError:
        return jsonify({"status": resp.status_code, "response": resp.text}), resp.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 7890))
    app.run(host="0.0.0.0", port=port)
