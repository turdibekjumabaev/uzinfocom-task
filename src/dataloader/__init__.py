from .role import load_roles
from .user import load_users


def load_data(db):
    load_roles(db)
    load_users(db)
