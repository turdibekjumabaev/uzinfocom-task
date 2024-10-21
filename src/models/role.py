from src.dp import db


class Role(db.Model):
    __tablename__ = 'roles'

    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(64), unique=True, nullable=False)

    users = db.relationship('User', backref='role', lazy=True)

    def __init__(self, role_name):
        self.role_name = role_name

    def __repr__(self):
        return '<Role %r>' % self.role_name

    def to_dict(self):
        return {
            'role_id': self.role_id,
            'role_name': self.role_name
        }
