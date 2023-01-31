from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import user_model
from flask import flash

db ='recipes_db'

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
    
    @classmethod
    def save_recipe(cls,data):
        query="INSERT INTO recipes(user_id, name, description, instructions, date_made, under_30) VALUES(%(user_id)s, %(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_30)s);"
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def get_all_recipes_creator(cls):
        query="SELECT * FROM recipes JOIN users ON users.id = recipes.user_id;"
        results = connectToMySQL(db).query_db(query)
        print(results)

        all_recipes=[] # we are going to get all recipes with its creator in our list
        for row in results:
            recipe_data={
                "id": row['id'],
                "user_id": row['user_id'],
                "name": row['name'],
                "description": row['description'],
                "instructions": row['instructions'],
                "date_made": row['date_made'],
                "under_30": row['under_30'],
                "created_at": row['created_at'],
                "updated_at": row['updated_at']
            }

            user_data={
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            one_recipe = cls(recipe_data)
            one_recipe.creator = user_model.User(user_data)

            all_recipes.append(one_recipe)

        return all_recipes
    
    @classmethod
    def get_one_recipe_w_user(cls, data):
        query="SELECT * FROM recipes JOIN users ON recipes.user_id= users.id WHERE recipes.id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        one_recipe = cls(results[0]) #grabbing the object
        user_data={
            "id": results[0]['users.id'],
            "first_name": results[0]['first_name'],
            "last_name": results[0]['last_name'],
            "email": results[0]['email'],
            "password": results[0]['password'],
            "created_at": results[0]['users.created_at'],
            "updated_at": results[0]['users.updated_at']
        }

        one_recipe.creator = user_model.User(user_data)
        return one_recipe
    
    @classmethod
    def update_recipe(cls, data):
        query="UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_made=%(date_made)s, under_30=%(under_30)s WHERE recipes.id=%(id)s;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def delete_recipe(cls, data):
        query="DELETE FROM recipes WHERE recipes.id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)
    
    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data['name'])< 3:
            flash("Recipe name min 3 characters")
            is_valid= False
        if len(data['description'])< 3:
            flash("Recipe description min 3 characters")
            is_valid= False
        if len(data['instructions'])< 3:
            flash("Recipe instructions min 3 characters")
            is_valid= False
        if len(data["date_made"]) <= 0:
            flash("Date is required.")
            is_valid = False

        if 'under_30'not in data:
            flash(" Does recipe take less than 30 mins?")
            is_valid= False
        return is_valid