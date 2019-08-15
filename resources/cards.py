from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from helpers import init_parser
from models.cards import CardModel
from models.cardcollections import CardCollectionModel


class Card(Resource):
    @jwt_required
    def get(self, col_id, card_id):
        user_id = get_jwt_identity()
        collection = CardCollectionModel.find_by_id(user_id, col_id)

        if collection:
            for card in collection.cards:
                if card.id == card_id:
                    return card.json()

        return {'message': 'Unable to find card'}, 404

    @jwt_required
    def post(self, col_id):
        parser = init_parser()
        parser.add_argument('question', type=str, required=True,
                            help="Question is required")
        parser.add_argument('answer', type=str, required=True,
                            help="Answer is required")
        parser.add_argument('hint', type=str, required=True,
                            help="Hint is required")

        user_id = get_jwt_identity()
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

    @jwt_required
    def put(self, col_id, card_id):
        parser = init_parser()
        parser.add_argument('question', type=str)
        parser.add_argument('answer', type=str)
        parser.add_argument('hint', type=str)
        parser.add_argument('learned', type=bool)

        user_id = get_jwt_identity()
        collection = CardCollectionModel.find_by_id(user_id, col_id)

        for card in collection.cards:
            if card.id == card_id:
                data = parser.parse_args()
                card.question = data['question']
                card.answer = data['answer']
                card.hint = data['hint']
                card.learned = data['learned']

                card.save_to_db()
                return card.json()

        return {'message': 'Unable to find card to update'}, 404

    @jwt_required
    def delete(self, col_id, card_id):
        user_id = get_jwt_identity()
        collection = CardCollectionModel.find_by_id(
            user_id, col_id)

        if collection:
            # Load the cards
            collection.cards.all()
            for card in collection.cards:
                if card.id == card_id:
                    card.delete_from_db()
            return {'message': 'Card deleted'}

        return {'message': 'Unable to delete card'}, 400
