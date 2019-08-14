from helpers import init_parser
from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse
from models.cards import CardModel, CardCollectionModel


class Card(Resource):
    @jwt_required()
    def get(self, col_id, card_id):
        user_id = current_identity.id
        collection = CardCollectionModel.find_by_id(user_id, col_id)

        if collection:
            for card in collection.cards:
                if card.id == card_id:
                    return card.json()

        return {'message': 'Unable to find card'}, 404

    @jwt_required()
    def post(self, col_id):
        parser = init_parser()
        parser.add_argument('question', type=str, required=True,
                            help="Question is required")
        parser.add_argument('answer', type=str, required=True,
                            help="Answer is required")
        parser.add_argument('hint', type=str, required=True,
                            help="Hint is required")

        user_id = current_identity.id
        collection = CardCollectionModel.find_by_id(user_id, col_id)

        if collection is None:
            return {'message': 'Unable to find subject'}, 404

        data = parser.parse_args()
        for card in collection.cards:
            if card.question == data['question']:
                return {'message': 'That question already exists'}, 400

        new_card = CardModel(collection.subject, **data)
        collection.cards.append(new_card)
        collection.save_to_db()

        return new_card.json()

    @jwt_required()
    def put(self, col_id, card_id):
        parser = init_parser()
        parser.add_argument('question', type=str)
        parser.add_argument('answer', type=str)
        parser.add_argument('hint', type=str)
        parser.add_argument('learned', type=bool)

        user_id = current_identity.id
        collection = CardCollectionModel.find_by_id(user_id, col_id)

        for card in collection.cards:
            if card.id == card_id:
                data = parser.parse_args()
                card.question = data['question']
                card.answer = data['answer']
                card.hint = data['hint']
                card.learned = data['learned']
                return card.json()

        return {'message': 'Unable to find card to update'}, 404

    @jwt_required()
    def delete(self, col_id, card_id):
        user_id = current_identity.id
        collection = CardCollectionModel.find_by_id(user_id, col_id)

        if collection:
            # Load the cards
            collection.cards.all()
            for card in collection.cards:
                if card.id == card_id:
                    card.delete_from_db()
            return {'message': 'Card deleted'}

        return {'message': 'Unable to delete card'}, 400


class CardCollection(Resource):

    # /collections/<int:col_id>
    @jwt_required()
    def get(self, col_id):
        user_id = current_identity.id
        collection = CardCollectionModel.find_by_id(user_id, col_id)

        if collection:
            return collection.json()

        return {'message': "Unable to find collection"}, 404

    # /collections/<int:col_id> - {string:new_subject}
    @jwt_required()
    def put(self, col_id):
        parser = init_parser()
        parser.add_argument('new_subject', type=str,
                            required=True, help="This field is required")

        data = parser.parse_args()
        user_id = current_identity.id
        existing_collection = CardCollectionModel.find_by_id(
            user_id, col_id)

        # Ensure that there isn't already a collection by this name
        if existing_collection and existing_collection.subject != data['new_subject']:
            existing_collection.subject = data['new_subject']
            existing_collection.save_to_db()

            return existing_collection.json()
        elif existing_collection and existing_collection.subject == data['new_subject']:
            return {'message': 'Subject already exists'}, 400

        return {'message': 'Unable to find subject'}, 404

    # /collections/<int:col_id>
    @jwt_required()
    def delete(self, col_id):
        user_id = current_identity.id
        collection = CardCollectionModel.find_by_id(user_id, col_id)

        if collection:
            collection.delete_from_db()

        return {'message': "Collection deleted"}


# This class handles operations in aggregate
class CardCollectionList(Resource):
    parser = init_parser()
    parser.add_argument('subject', type=str, required=True,
                        help='A subject is required')

    # /collections
    @jwt_required()
    def get(self):
        user_id = current_identity.id
        collections = CardCollectionModel.query.filter_by(
            user_id=user_id).all()

        if collections:
            return {'collections': [collection.json() for collection in collections]}

        return {'message': 'Unable to load collections'}, 404

    # /collections - {string:subject}
    @jwt_required()
    def post(self):
        parser = init_parser()
        parser.add_argument('subject', type=str, required=True,
                            help="A subject is required")
        data = parser.parse_args()
        user_id = current_identity.id
        collection = CardCollectionModel.find_by_subject(
            user_id, data['subject'])

        if collection:
            return {'message': 'That subject already exists'}, 400

        new_collection = CardCollectionModel(current_identity.id, **data)
        new_collection.save_to_db()

        return new_collection.json()
