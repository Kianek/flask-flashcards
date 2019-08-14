from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse
from helpers import init_parser
from models.cardcollections import CardCollectionModel


class CardCollection(Resource):

    # /collections/<int:col_id>
    # Get all collections for the current user.
    @jwt_required()
    def get(self, col_id):
        user_id = current_identity.id
        collection = CardCollectionModel.find_by_id(user_id, col_id)

        if collection:
            return collection.json()

        return {'message': "Unable to find collection"}, 404

    # /collections/<int:col_id> - {string:new_subject}
    # Update a single flash card.
    @jwt_required()
    def put(self, col_id):
        parser = init_parser()
        parser.add_argument('new_subject', type=str,
                            required=True, help="This field is required")
        data = parser.parse_args()

        existing_collection = CardCollectionModel.find_by_id(
            current_identity.id, col_id)

        # Ensure that there isn't already a collection by this name
        if existing_collection and existing_collection.subject != data['new_subject']:
            existing_collection.subject = data['new_subject']
            existing_collection.save_to_db()

            return existing_collection.json()
        elif existing_collection and existing_collection.subject == data['new_subject']:
            return {'message': 'Subject already exists'}, 400

        return {'message': 'Unable to find subject'}, 404

    # /collections/<int:col_id>
    # Delete a single collection.
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
    # Get all of the current user's flash card collections.
    @jwt_required()
    def get(self):
        user_id = current_identity.id
        collections = CardCollectionModel.query.filter_by(
            user_id=user_id).all()

        if collections:
            return {'collections': [collection.json() for collection in collections]}

        return {'message': 'Unable to load collections'}, 404

    # /collections - {string:subject}
    # Add a new collection.
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
