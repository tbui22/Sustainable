from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Item:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.quantity = data['quantity']
        self.restock_date = data['restock_date']
        self.user_id = data['user_id']
        self.category_id = data['category_id']
        self.shopping_list_id = data['shopping_list_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @staticmethod
    def validateItem(form_data):
        is_valid = True

        if not form_data['name'] or not form_data['quantity'] or not form_data['restock_date']:
            flash ("Please fill in all fields")
            is_valid = False

        return is_valid 

    @classmethod
    def showItemsCategory(cls, data):
        query = "SELECT * FROM items WHERE category_id= %(id)s and user_id= %(user_id)s;"
        return connectToMySQL('python_project').query_db(query, data)

    @classmethod
    def showCateory(cls, data):
        query = "SELECT * FROM categories WHERE id = %(id)s;"
        return connectToMySQL('python_project').query_db(query, data)

    @classmethod
    def saveItem(cls, data):
        query = "INSERT INTO items (name, quantity, restock_date, category_id, user_id, created_at, updated_at) VALUES (%(name)s, %(quantity)s, %(restock_date)s, %(category_id)s, %(user_id)s, now(), now());"
        return connectToMySQL('python_project').query_db(query, data)
    
    @classmethod   
    def edit_item(cls, data):
        query = "UPDATE items SET name = %(name)s, quantity = %(quantity)s, restock_date = %(restock_date)s, updated_at = now() WHERE id = %(id)s AND user_id = %(user_id)s;"
        return connectToMySQL('python_project').query_db( query, data)
    
    @classmethod
    def delete_item(cls, data):
        query =  "DELETE FROM items WHERE id = %(id)s;"
        return connectToMySQL('python_project').query_db(query, data)

    @classmethod
    def getAllItemsByCategory(cls):
        query = "SELECT * FROM categories LEFT JOIN items ON items.category_id = categories.id;"
        return connectToMySQL('python_project').query_db(query)
    
    @classmethod
    def appendtoList(cls, data):
        query = "UPDATE items SET shopping_list_id = ( %(shoppinglist_id)s) WHERE id = %(item_id)s;"
        return connectToMySQL('python_project').query_db(query, data)
    
    @classmethod
    def deletefromList(cls, data):
        query = "UPDATE items SET shopping_list_id = 0 WHERE id = %(item_id)s;"
        return connectToMySQL('python_project').query_db(query, data)

    @classmethod
    def showList(cls, data):
        query = "SELECT * FROM items WHERE shopping_list_id = %(shopping_list_id)s;"
        print(query)
        return connectToMySQL('python_project').query_db(query, data)
    
    @classmethod
    def showAllItems(cls, data):
        query = "SELECT * FROM items WHERE user_id = %(id)s;"
        return connectToMySQL('python_project').query_db(query, data)

