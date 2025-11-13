import os

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from .config import config

load_dotenv()


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()


def create_app(
    config_name: str = os.environ.get("FLASK_CONFIG", "development")
) -> Flask:
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    print(f"Running in config: {config_name}")

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from . import views
        views.register_routes(app)

        from .users import users_bp
        from .products import products_bp
        from .posts import posts_bp

        app.register_blueprint(users_bp)
        app.register_blueprint(products_bp)
        app.register_blueprint(posts_bp)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    return app
