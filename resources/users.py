from flask_jwt_extended import create_access_token, create_refresh_token, fresh_jwt_required
from flask_restful import Resource
from helpers import init_parser
from models.users import UserModel

_parser = init_parser()
_parser.add_argument('username', type=str, required=True,
                     help="Username must be unique")
_parser.add_argument('password', type=str, required=True,
                     help="Password is required")


class UserRegister(Resource):
    # /register - {string:username, string:password}
    def post(self):
        data = _parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'That username is already registered'}, 400

        new_user = UserModel(**data)
        new_user.save_to_db()

        return {'message': 'User created successfully'}, 201

    # /delete - {int:user_id}
    @fresh_jwt_required
    def delete(self):
        parser = init_parser()
        parser.add_argument('user_id', type=int,
                            required=True, help="User ID is required")
        data = parser.parse_args()

        user_to_delete = UserModel.find_by_id(data['user_id'])

        if user_to_delete:
            try:
                user_to_delete.delete_from_db()
                return {'message': 'Account deleted'}, 200
            except:
                return {'message': 'Unable to delete account'}, 500

        return {'message': 'Unable to locate user'}, 404


class UserLogin(Resource):

    @classmethod
    def post(cls):
        from app import flask_bcrypt
        data = _parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user and flask_bcrypt.check_password_hash(user.password_hash, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)

            return {'access_token': access_token, 'refresh_token': refresh_token}, 200

        return {'message': 'Invalid credentials'}, 401
