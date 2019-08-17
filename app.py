from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restful import Api, Resource
from db import db
from resources.cards import Card
from resources.cardcollections import CardCollection, CardCollectionList
from resources.users import UserRegister, UserLogin

app = Flask(__name__)
migrate = Migrate(app, db)
app.config.from_pyfile('settings.py')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
flask_bcrypt = Bcrypt(app)
api = Api(app)

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

db.init_app(app)

if __name__ == '__main__':

    @app.before_first_request
    def create_tables():
        db.create_all()

    app.run()
