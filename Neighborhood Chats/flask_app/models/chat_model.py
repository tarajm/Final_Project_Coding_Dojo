from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user_model
from flask import flash

db = 'users_and_chats_w_messages'
# db = 'neighborhood_chats'


class Chat:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.location = data['location']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM chats JOIN users ON chats.users_id = users.id WHERE chats.id = %(id)s;"
        results = connectToMySQL(db).query_db(query,data)
        print(results[0])
        chat = cls(results[0])
        chat.posted_by = results[0]["fname"] + " " + results[0]["lname"]
        chat.users_id = results[0]["users_id"]
        return chat

    @classmethod
    def get_chats_w_user(cls, data):
        query = "SELECT * FROM chats JOIN users ON chats.users_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        chats = []
        for chat in results:
            chats.append(cls(chat))
        return chats
    
    @classmethod
    def get_all_chats_with_users(cls):
        query = "SELECT * FROM chats JOIN users ON chats.users_id = users.id;"
        results = connectToMySQL(db).query_db(query)
        all_chats = []
        for chat in results:
            one_chat = cls(chat)
            one_chat_user_info = {
                "id": chat['users.id'], 
                "fname": chat['fname'],
                "lname": chat['lname'],
                "email": chat['email'],
                "password": chat['password'],
                "created_at": chat['users.created_at'],
                "updated_at": chat['users.updated_at']
            }
            user_of_chat = user_model.User(one_chat_user_info)
            one_chat.user = user_of_chat
            all_chats.append(one_chat)
        return all_chats

    @classmethod
    def add_chat(cls, data):
        query = "INSERT INTO chats (name, description, location, date, created_at, users_id) VALUES ( %(name)s, %(description)s, %(location)s, %(date)s, NOW(), %(users_id)s );"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def delete_chat(cls, data):
        query = "DELETE FROM chats WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def update_chat(cls, data):
        query = "UPDATE chats SET name = %(name)s, description = %(description)s, location = %(location)s, date = %(date)s, updated_at = NOW(), users_id = %(users_id)s WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM chats WHERE id = %(id)s"
        result = connectToMySQL(db).query_db(query,data)
        return cls(result[0])

    @staticmethod
    def validate_chat(chats):
        is_valid = True
        if len(chats['name']) <= 0:
            flash("Name field cannot be left blank!")
            is_valid = False
        if len(chats['description']) <= 0:
            flash("Description field cannot be left blank!")
            is_valid = False
        if len(chats["location"]) <= 0:
            flash("Location field cannot be left blank!")
            is_valid = False
        if len(chats['date']) <=0:
            flash("Date must be greater than 0!")
            is_valid = False
        return is_valid

