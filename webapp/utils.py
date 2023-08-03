from webapp.model import User


def get_admin_id():
    admin_id = None
    admin = User.query.filter(User.name == "admin").one_or_none()

    if admin:
        admin_id = admin.id

    return admin_id
