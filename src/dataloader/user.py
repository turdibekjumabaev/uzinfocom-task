from src.models.user import User
from src.models.role import Role


def load_users(db):
    admin_role = Role.query.filter_by(role_name='ADMIN').first()
    admin_data = {
        'first_name': 'Uzinfocom',
        'last_name': 'Task',
        'mobile_phone': '998998887766',
        'password': '1234',
        'role_id': admin_role.role_id
    }

    admin = User.query.filter_by(mobile_phone=admin_data['mobile_phone']).first()

    if admin is None:
        admin = User(**admin_data)
        db.session.add(admin)

    db.session.commit()
