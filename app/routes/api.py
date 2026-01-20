import os
import json
from flask import Blueprint, jsonify, request, current_app

api_bp = Blueprint("api", __name__)


@api_bp.route("/api/credentials/<platform>")
def get_credentials(platform):
    path = current_app.config["MODULE_PATHS"].get(platform)
    if not path:
        return jsonify({"error": "Platform not found"}), 404

    accounts = []
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                accounts = json.load(f)
        except Exception as e:
            print(f"Error reading {path}: {e}")

    schema = current_app.config["MODULE_SCHEMAS"].get(platform, [])
    if not schema and accounts:
        schema = list(accounts[0].keys())

    return jsonify({"accounts": accounts, "schema": schema})


@api_bp.route("/credentials/update", methods=["POST"])
def update_credentials():
    data = request.json
    platform = data.get("platform")
    new_account = data.get("account_data")

    path = current_app.config["MODULE_PATHS"].get(platform)
    if not path or not new_account:
        return jsonify({"error": "Invalid data"}), 400

    accounts = []
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                accounts = json.load(f)
        except:
            pass

    accounts.append(new_account)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as f:
        json.dump(accounts, f, indent=4)

    return jsonify({"status": "success"})
