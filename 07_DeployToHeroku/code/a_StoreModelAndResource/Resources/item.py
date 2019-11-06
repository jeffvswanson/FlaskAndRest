from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from Models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")
    parser.add_argument('store_id', type=int, required=True, help='Every item needs a store ID!')

    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            {'message': 'An error occurred attempting to retrieve the item from the database.'}, 500  # Internal Server Error
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404  # Not found

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400  # Bad Request

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item into the database.'}, 500  # Internal Server Error

        return item.json(), 201 # Created

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            try:
                item = ItemModel(name, **data)
            except:
                {'message': 'An error occurred attempting to insert the item into the database'}, 500  # Internal Server Error
        else:
            try:
                item.price = data['price']
                item.store_id = data['store_id']
            except:
                {'message': 'An error occurred attempting to update the item in the database'}, 500  # Internal Server Error

        item.save_to_db()

        return item.json()

class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}