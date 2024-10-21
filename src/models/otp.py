from src.dp import db

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta


class OTP(db.Model):
    __tablename__ = 'otp'

    otp_id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(50))
    otp_hash = db.Column(db.String, nullable=False)
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    expires_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, phone):
        self.phone = phone

    def __repr__(self):
        return f'<OTP {self.otp_id} for User {self.user_id}>'

    def set_otp(self, otp_code, expires_in=300):
        self.otp_hash = generate_password_hash(otp_code)
        self.expires_at = datetime.now() + timedelta(seconds=expires_in)

    def check_otp(self, otp_code):
        return check_password_hash(self.otp_hash, otp_code)

    def is_expired(self):
        return datetime.now() > self.expires_at and not self.used

    def mark_as_used(self):
        self.used = True
