from db import db


class CardCollectionModel(db.Model):
    __tablename__ = 'collections'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    subject = db.Column(db.String(80))

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("UserModel", back_populates="collections")

    cards = db.relationship(
        'CardModel', cascade="save-update, delete", lazy='dynamic', back_populates="collection")

    def __init__(self, user_id, subject):
        self.user_id = user_id
        self.subject = subject

    def json(self):
        return {'id': self.id, 'user_id': self.user_id, 'subject': self.subject, 'cards': [card.json() for card in self.cards.all()]}

    @classmethod
    def find_by_subject(cls, user_id, subject):
        return cls.query.filter_by(user_id=user_id, subject=subject).first()

    @classmethod
    def find_by_id(cls, user_id, col_id):
        return cls.query.filter_by(user_id=user_id, id=col_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
