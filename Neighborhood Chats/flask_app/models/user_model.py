from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask import flash
from flask_app.models import chat_model

db = 'users_and_chats_w_messages'
# db = 'neighborhood_chats'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.fname = data['fname']
        self.lname = data['lname']
        self.email= data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.chat = []


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(db).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL(db).query_db(query,data)
        return cls(result[0])

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def create(cls,data):
        query = "INSERT INTO users (fname, lname, email, password, created_at) VALUES ( %(fname)s,%(lname)s,%(email)s,%(password)s, NOW());"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def update(cls,data):
        query = "UPDATE users SET NAME fname = %(fname)s, lname = %(lname)s, email = %(email)s, password = %(password)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)

    @staticmethod
    def is_valid_reg(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query, user)
        if len(results) >= 1:
            flash("Email already taken!!", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email Address!", "register")
            is_valid = False
        if len(user['fname']) <= 3:
            flash("First name must be AT LEAST 3 characters!", "register")
            is_valid = False
        if len(user['lname']) <= 3:
            flash("Last name must be AT LEAST 3 characters!", "register")
            is_valid = False
        if len(user['password']) <= 8:
            flash("Password must be AT LEAST 8 characters!", "register")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords do NOT match! Try again!", "register")
            is_valid = False
        return is_valid
    
    @staticmethod
    def is_valid_zip(zip):
        print('zip',zip)
        is_valid = True
        if len(zip['zipcode']) <5:
            flash("Zipcode must be at least 5 digits long. Try again.")
            is_valid = False
        if len(zip['zipcode']) >5:
            flash("Zipcode cannot be longer than 5 digits. Try again.")
            is_valid = False
        if not zip['zipcode'].isnumeric():
            flash("Zipcode must be only numbers. Try again.")
            is_valid = False
        return is_valid