from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate(form_data):
        is_valid = True

        if len(form_data["first_name"]) <2 :
            flash("First Name must be greater than 2 characters!!")
            is_valid = False
            return is_valid

        if not form_data['first_name'].isalpha():
            flash("First name can only consist of letters!!")
            is_valid = False
            return is_valid

        if len(form_data["last_name"]) <2 :
            flash("Last Name must be greater than 2 characters!!")
            is_valid = False
            return is_valid

        
        if not form_data['last_name'].isalpha():
            flash("Last name can only consist of letters!!")
            is_valid = False
            return is_valid


        emailData = form_data["email"]
        existingEmails = User.get_all()
        for existingEmail in existingEmails:
            if existingEmail.email == emailData:
                flash("Email is already in database!")
                is_valid= False
                return is_valid

        if not EMAIL_REGEX.match(emailData):
            flash("Invalid email address!")
            is_valid = False
            return is_valid


        if len(form_data["password"]) <8 :
            flash("Password must be at least 8 characters long!")
            is_valid = False
            return is_valid


        if form_data["password"] != form_data["confirmPassword"] :
            flash("Password and Password Confirmation must match!")
            is_valid = False
            return is_valid

        return is_valid

    @classmethod
    def showOneUser(cls, data):
        query = "SELECT * FROM users WHERE id= %(id)s;"
        result = connectToMySQL('python_project').query_db(query, data)
        return cls(result[0])

# save info into database
    @classmethod
    def saveInfo(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, now(), now());"
        return connectToMySQL('python_project').query_db(query, data)

    @classmethod
    def createShoppingList(cls, data): 
        query = "INSERT INTO shopping_lists (user_id) VALUES ( %(user_id)s);"
        return connectToMySQL('python_project').query_db(query, data)

# get all the rows within a table
    @classmethod
    def get_all(cls):
            query = "SELECT * FROM users;"
            results = connectToMySQL('python_project').query_db(query)
            users = []
            for user in users:
                users.append(cls(users))
            for user in users:
                print(user.id)
                
            return users

    @classmethod
    def get_by_email(cls, data):
        query =" SELECT * FROM users WHERE email= %(email)s;"
        result = connectToMySQL('python_project').query_db(query, data)
        if len (result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def getShoppingList(cls, data):
        query = "SELECT * FROM shopping_lists WHERE user_id = %(id)s;"
        print(query)
        result = connectToMySQL('python_project').query_db(query, data)
        return result
