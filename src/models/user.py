from werkzeug.security import generate_password_hash, check_password_hash

from src.dp import db


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50))
    mobile_phone = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'), nullable=False)

    def __init__(self, first_name, last_name, mobile_phone, role_id, password=None):
        self.first_name = first_name
        self.last_name = last_name
        self.mobile_phone = mobile_phone
        self.role_id = role_id
        if password is not None:
            self.password = generate_password_hash(password)
        else:
            self.password = None

    def __repr__(self):
        return '<User %r>' % self.user_id

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'mobile_phone': self.mobile_phone,
            'role_id': self.role_id
        }
