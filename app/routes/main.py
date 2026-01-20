from flask import Blueprint, render_template, current_app

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    modules = list(current_app.config["MODULE_PATHS"].keys())
    return render_template("dashboard.html", modules=modules)


@main_bp.route("/credentials")
def credentials():
    modules = list(current_app.config["MODULE_PATHS"].keys())
    return render_template("credentials.html", module_keys=modules)
