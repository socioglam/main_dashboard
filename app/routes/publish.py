from flask import (
    Blueprint,
    request,
    Response,
    stream_with_context,
    current_app,
    jsonify,
)
import os
import json
from app.utils.logger import Logger
from app.services.poster_service import start_poster_thread

publish_bp = Blueprint("publish", __name__)


@publish_bp.route("/publish", methods=["POST"])
def publish():
    req_data = request.json
    target_platform = req_data.get("platform")

    logger = Logger()

    # We pass necessary config to the background thread
    module_paths = current_app.config["MODULE_PATHS"]
    source_url = current_app.config["SOURCE_API_URL"]

    start_poster_thread(logger, target_platform, module_paths, source_url)

    def generate():
        while True:
            msg = logger.get_queue().get()
            if msg is None:
                break
            yield msg

    return Response(stream_with_context(generate()), mimetype="text/plain")


@publish_bp.route("/report", methods=["GET"])
def get_report():
    report_path = os.path.join(os.getcwd(), "app", "latest_report.json")
    if os.path.exists(report_path):
        try:
            with open(report_path, "r") as f:
                data = json.load(f)
            return jsonify(data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "No report found"}), 404
