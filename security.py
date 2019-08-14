from werkzeug.security import safe_str_cmp
from models.users import UserModel


def authenticate(username, password):
    from app import flask_bcrypt

    user = UserModel.find_by_username(username)
    if user and flask_bcrypt.check_password_hash(user.password_hash, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
