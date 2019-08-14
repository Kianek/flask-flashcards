from flask_restful import Resource
from helpers import init_parser
from models.users import UserModel


class UserRegister(Resource):
    parser = init_parser()
    parser.add_argument('username', type=str, required=True,
                        help="Username must be unique")
    parser.add_argument('password', type=str, required=True,
                        help="Password is required")

    # /register - {string:username, string:password}
    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'That username is already registered'}, 400

        new_user = UserModel(**data)
        new_user.save_to_db()

        return {'message': 'User created successfully'}, 201
