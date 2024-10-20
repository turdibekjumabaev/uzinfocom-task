from flask import Flask

from src.routes import init_routes
from src.models import init_db


def init_app(app: Flask):
    app.config.from_object('src.config.Config')
    init_routes(app)
    init_db(app)
