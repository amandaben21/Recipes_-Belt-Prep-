from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import recipe_model
from flask import flash
from flask_bcrypt import Bcrypt
import re
EMAIL_REGEX= re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)

db ='recipes_db'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes=[] 
    
    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(db).query_db(query)
        print(results)
        users_list= []

        for user in results:
            users_list.append(cls(user))
        return users_list

    # @classmethod
    # def get_all_users_with_orders(cls):
    #     query = "SELECT * FROM users JOIN cookies ON users.id = cookies.user_id;"
    #     results = connectToMySQL(db).query_db(query)
    #     print(results)
    #     users_list= []
    #     #creating a dictionary that captures the user information in a row
    #     for row in results:
    #         cookie_data={
    #             "id":row['cookies.id'],
    #             "user_id":row['user_id'],
    #             "name":row['name'],
    #             "cookie_type":row['cookie_type'],
    #             "num_boxes": row['num_boxes'],
    #             "created_at":row['created_at'],
    #             "updated_at":row['updated_at']
    #         }
    #         one_order = cookie_order.Cookie_order(cookie_data)

    #         user_data={
    #             "id":row['id'],
    #             "first_name":row['first_name'],
    #             "last_name":row['last_name'],
    #             "email":row['email'],
    #             "password":row['password'],
    #             "created_at":row['created_at'],
    #             "updated_at":row['updated_at']
    #         }
    #         one_user = cls(user_data)
    #         one_user.orders.append(one_order)
    #         users_list.append(one_user)
    #     return users_list

    @classmethod
    def get_one_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        one_user = cls(results[0])
        return one_user

    @classmethod
    def get_one_user_w_recipes(cls, data):
        query="SELECT * FROM users LEFT JOIN recipes ON recipes.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        one_user = cls(results[0])
        for row in results:
            recipe_data={
                "id": row['recipes.id'],
                "user_id": row['user_id'],
                "name": row['name'],
                "description": row['description'],
                "instructions": row['instructions'],
                "date_made": row['date_made'],
                "under_30": row['under_30'],
                "created_at": row['recipes.created_at'],
                "updated_at": row['recipes.updated_at']
            }
            one_recipe= recipe_model.Recipe(recipe_data)
            one_user.recipes.append(one_recipe)
        return one_user

    @classmethod
    def save_user(cls, form_data):
        hash_pword= bcrypt.generate_password_hash(form_data['password']) #password comes from route which comes from the form name=password
        user_data={
            "first_name": form_data['first_name'],
            "last_name": form_data['last_name'],
            "email": form_data['email'],
            "password": hash_pword
        }
        query="INSERT INTO users(first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(db).query_db(query, user_data)

    @classmethod
    def get_email(cls,data):
        query="SELECT * FROM users WHERE email=%(email)s;"
        result= connectToMySQL(db).query_db(query,data)
        if len(result)<1:
            return False
        one_user= cls(result[0])
        print(one_user.password)
        return one_user

    @staticmethod
    def validate_register(form_data):
        is_valid = True

        if len(form_data['first_name']) < 2: #first_name is same as the form in log_reg.html in register method post
            flash("First Name Must be At Least 2 Letters", "register")
            is_valid = False #we include switching the value to false b/c its tigger to a false it triggers the validated warnings on the frontend

        if len(form_data['last_name']) < 2: #last_name is same as the form in log_reg.html in register method post
            flash("Last Name Must be At Least 2 Letters", "register")
            is_valid = False
        
        if not EMAIL_REGEX.match(form_data['email']):
            flash("You Must Enter A Vaild Email", "register")   #register for the category_filter=["register"] in log_reg.html
            is_valid = False

        
        if form_data['password'] != form_data['confpassword']:
            flash("Password Does Not Match", "register")
            is_valid = False

        if len(form_data['password']) < 8:
            flash("Password Must Be At Least 8 Characters", "register")
            is_valid = False

        return is_valid
    
    @staticmethod
    def validate_login(form_data):
        is_valid = True
        #to avoid mapping issues we create a dictionary ece out the data
        user_email={
            "email":form_data['email']
        }
        user_exists= User.get_email(user_email)

        if not user_exists:
            flash("Ivalid email/password", "login")   #login for the category_filter=["login"] in log_reg.html
            is_valid=False
        if user_exists:
            if not bcrypt.check_password_hash(user_exists.password, form_data['password']):
                flash("Invalid email/password", "login")
                is_valid=False
        return is_valid