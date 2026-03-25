from flask import Flask

from .config import Config
from .db import init_engine, remove_session


def format_metric(value):
    if value is None:
        return "N/A"
    return f"{value:g}"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_engine(app.config["DATABASE_URL"])
    app.teardown_appcontext(remove_session)
    app.jinja_env.filters["metric"] = format_metric

    from .routes import bp

    app.register_blueprint(bp)
    return app
