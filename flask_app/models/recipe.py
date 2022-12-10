from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session
from flask_app.models import user


class Recipe:
    DB = "recipe_share"

    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_cooked = data['date_cooked']
        self.under = data['under']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.creator = None

    @classmethod
    def create_recipe(cls, recipe_data):
        data ={
            "name": recipe_data['name'],
            "description": recipe_data['description'],
            "instructions": recipe_data['instructions'],
            "date_cooked": recipe_data['date_cooked'],
            "under": recipe_data['under'],
            "user_id": session["user_id"]
        }

        query = """
                INSERT INTO recipes (name, description, instructions, date_cooked, under, user_id, created_at, updated_at)
                VALUES (%(name)s,%(description)s,%(instructions)s,%(date_cooked)s,%(under)s,%(user_id)s, NOW(), NOW());
                """

        results = connectToMySQL(cls.DB).query_db(query, data)

        return results


    @classmethod 
    def all_recipes_with_creator(cls):
        query = """
                SELECT * FROM recipes
                JOIN users
                ON recipes.user_id = users.id
                ORDER by recipes.created_at DESC;
                """
        results = connectToMySQL(cls.DB).query_db(query)
        all_recipes= []

        for recipe in results:
            one_recipe = cls(recipe)

            user_data = {
                "id": recipe['users.id'],
                "first_name": recipe['first_name'],
                "last_name": recipe['last_name'],
                "email": recipe['email'],
                "password": recipe['password'],
                "created_at": recipe['users.created_at'],
                "updated_at": recipe['users.updated_at']
            }

            one_recipe.creator = user.User(user_data)

            all_recipes.append(one_recipe)

        return all_recipes


    @classmethod
    def one_recipe_with_creator(cls, recipe_data):
        data = {
            "id": recipe_data
        }
        query = """
                SELECT * FROM recipes
                JOIN users
                ON recipes.user_id = users.id
                WHERE recipes.id = %(id)s;
                """

        results = connectToMySQL(cls.DB).query_db(query,data)

        recipe = cls(results[0])

        for col in results:
            data = {
                "id": col['users.id'],
                "first_name": col['first_name'],
                "last_name": col['last_name'],
                "email": col['email'],
                "password": col['password'],
                "created_at": col['users.created_at'],
                "updated_at": col['users.updated_at']
            }

            recipe.creator = user.User(data)

        return recipe



    @classmethod
    def select_by_id(cls, recipe_data):
        data = {
            "id": recipe_data
        }
        query = """
                SELECT * FROM recipes
                WHERE id = %(id)s
                """

        results = connectToMySQL(cls.DB).query_db(query,data)

        recipe = cls(results[0])

        return recipe

    @classmethod
    def update_recipe(cls, recipe_data):
        data = {
            "id": recipe_data['id'],
            "name": recipe_data['name'],
            "description": recipe_data['description'],
            "instructions": recipe_data['instructions'],
            "date_cooked": recipe_data['date_cooked'],
            "under": recipe_data['under']
        }
        query = """
                UPDATE recipes
                SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_cooked = %(date_cooked)s, under = %(under)s, updated_at = NOW()
                WHERE id = %(id)s;
                """

        return connectToMySQL(cls.DB).query_db(query, data)


    @classmethod 
    def delete(cls, recipe_data):
        data = {
            "id": recipe_data
        }
        query = """
                DELETE FROM recipes 
                WHERE id = %(id)s;
                """

        return connectToMySQL(cls.DB).query_db(query,data)


    @staticmethod
    def validate_recipe(recipe_data):
        is_valid = True

        if not recipe_data['name']:
            flash("name is required", "recipe")
            is_valid = False

        elif len(recipe_data['name']) < 3:
            flash("name must be at least 3 characters long.", "recipe")
            is_valid = False

        if not recipe_data['description']:
            flash("Description must not be blank.", "recipe")
            is_valid = False

        elif len(recipe_data['description']) < 3:
            flash("Description must be at least 3 characters long.", "recipe")
            is_valid = False

        if not recipe_data['instructions']:
            flash("Instructions must not be blank", "recipe")
            is_valid = False

        elif len(recipe_data['intructions']) < 3:
            flash("instructions must be at least 3 characters long.", "recipe")
            is_valid = False

        # if not recipe_data['date_cooked']:
        #     flash("Must pick date", "recipe_date")
        #     is_valid= False

        # if not recipe_data['under']:
        #     flash("Time is required", "recipe_date")
        #     is_valid= False
        print("__THIS IS VALID VAR___", is_valid)
        return is_valid








