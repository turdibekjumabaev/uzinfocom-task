from flask import Flask, Blueprint

from .otp import otp_bp
from .auth import auth_bp

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return "Running..."


def init_routes(app: Flask):
    app.register_blueprint(main_bp)
    app.register_blueprint(otp_bp, url_prefix='/api/otp')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
