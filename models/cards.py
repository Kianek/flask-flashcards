from db import db


class CardModel(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # title = db.Column(db.String(80))

    subject = db.Column(db.String(80))

    question = db.Column(db.String(240), unique=True)

    answer = db.Column(db.String(240))

    hint = db.Column(db.String(240))

    learned = db.Column(db.Boolean, default=False)

    # Relationships
    collection_id = db.Column(db.Integer, db.ForeignKey('collections.id'))
    collection = db.relationship('CardCollectionModel', back_populates="cards")

    # def __init__(self, title, subject, question, answer, hint):
    def __init__(self, subject, question, answer, hint):
        self.question = question
        self.subject = subject
        self.answer = answer
        self.hint = hint

    # Relationships
    collection_id = db.Column(db.Integer, db.ForeignKey(
        'collections.id'), nullable=False)
    collection = db.relationship('CardCollectionModel')

    def json(self):
        return {'id': self.id, 'collection_id': self.collection_id, 'subject': self.subject, 'question': self.question, 'answer': self.answer, 'hint': self.hint, 'learned': self.learned}

    # @classmethod
    # def find_by_title(cls, title):
    #     return cls.query.filter_by(title=title).first()

    @classmethod
    def find_by_subject(cls, subject):
        return cls.query.filter_by(subject=subject).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


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
