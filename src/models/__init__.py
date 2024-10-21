from src.dp import db
from src.dataloader import load_data


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        load_data(db)


# Models
from .otp import OTP
from .role import Role
from .user import User
