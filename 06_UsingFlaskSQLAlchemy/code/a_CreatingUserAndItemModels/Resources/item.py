import sqlite3
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from Models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")

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

        item = ItemModel(name, data['price'])
        try:
            item.insert()
        except:
            return {'message': 'An error occurred inserting the item into the database.'}, 500  # Internal Server Error

        return item, 201 # Created

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        try:
            item = ItemModel.find_by_name(name)
        except:
            {'message': 'An error occurred attempting to retrieve the item from the database.'}, 500  # Internal Server Error
        updated_item = ItemModel(name, data['price'])

        if item is None:
            try:
                updated_item.insert()
            except:
                {'message': 'An error occurred attempting to insert the item into the database'}, 500  # Internal Server Error
        else:
            try:
                updated_item.update()
            except:
                {'message': 'An error occurred attempting to update the item in the database'}, 500  # Internal Server Error
        return updated_item.json()

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)

        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()

        return {'items': items}