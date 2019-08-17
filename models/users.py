from db import db
from helpers import hash_password


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.String(80))

    email = db.Column(db.String(80))

    password_hash = db.Column(db.String(256))

    #  Relationships
    collections = db.relationship("CardCollectionModel", back_populates="user")

    def __init__(self, username, password):
        self.username = username
        self.password_hash = hash_password(password)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
