import sqlite3
from flask_restful import Resource, reqparse

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))  # (<value>,) = single value tuple
        row = result.fetchone()
        if row:
            # from db, column 0 = id, 1 = username, 2 = password
            # *row expands the arguments in row
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))  # (<value>,) = single value tuple
        row = result.fetchone()
        if row:
            # from db, column 0 = id, 1 = username, 2 = password
            # *row expands the arguments in row
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

class UserRegister(Resource, User):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field cannot be blank!")
    parser.add_argument('password', type=str, required=True, help="This field cannot be blank!")

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400  # Bad request

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # VALUES tuple = (id, username, password).
        # id is autoincremented by database as primary key, so must be NULL.
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message": "User created successfully."}, 201  # Created