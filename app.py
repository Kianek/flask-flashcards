from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restful import Api, Resource

from resources.cards import Card
from resources.cardcollections import CardCollection, CardCollectionList
from resources.users import UserRegister, UserLogin

app = Flask(__name__, instance_relative_config=True)
flask_bcrypt = Bcrypt(app)
app.config.from_pyfile('config.py')
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()

# Sanity check


class HelloWorld(Resource):
    def get(self):
        return "Hello, world!"


api.add_resource(HelloWorld, "/test")

jwt = JWTManager(app)

# Routes
api.add_resource(UserLogin, '/login')
api.add_resource(UserRegister, '/register', '/delete')
api.add_resource(CardCollection, '/collections/<int:col_id>')
api.add_resource(CardCollectionList, '/collections')
api.add_resource(Card, '/collections/<int:col_id>/cards/<int:card_id>',
                 '/collections/<col_id>/cards')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run()
